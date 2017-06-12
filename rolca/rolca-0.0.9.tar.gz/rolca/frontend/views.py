""".. Ignore pydocstyle D400.

==============
Frontend views
==============

.. autofunction:: rolca.frontend.views.upload_view

.. autoclass:: rolca.frontend.views.SelectContestView
    :members:

"""
from datetime import datetime

from django.contrib import messages
from django.core.exceptions import ValidationError
from django.db import transaction
from django.forms import formset_factory
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import TemplateView
from django.views.generic.list import ListView

from rolca.core.models import Contest, Theme
from rolca.frontend.decorators import check_contest_login_required
from rolca.frontend.forms import AuthorForm, PhotoForm


@check_contest_login_required
def upload_view(request, *args, **kwargs):
    """View for uploading photos."""
    contest = get_object_or_404(Contest, pk=kwargs.pop('contest_id'))

    initial_author = {}
    if request.user.is_authenticated():
        initial_author['first_name'] = request.user.first_name
        initial_author['last_name'] = request.user.last_name
        initial_author['email'] = request.user.email

    author_form = AuthorForm(request.POST or None, prefix='author', initial=initial_author)
    if not request.user.is_authenticated():
        author_form.fields['email'].required = True

    theme_formsets = []
    for theme in Theme.objects.filter(contest=contest).order_by('pk'):
        form_set = formset_factory(PhotoForm, extra=theme.n_photos, max_num=theme.n_photos)
        theme_formsets.append({
            'theme': theme,
            'formset': form_set(request.POST or None, request.FILES or None, prefix=theme.pk),
        })

    if request.method == 'POST':
        try:
            with transaction.atomic():
                user = request.user if request.user.is_authenticated() else None

                if not author_form.is_valid():
                    raise ValidationError('Author form is not valid')
                author = author_form.save(commit=False)
                author.user = user
                author.save()

                photo_count = 0
                for formset_obj in theme_formsets:
                    formset = formset_obj['formset']
                    theme = formset_obj['theme']

                    for form in formset:
                        if not form.is_valid():
                            raise ValidationError('Photo form is not valid')
                        # validation returns True for empty forms in formset, so
                        # we have to check that there are actual data to save
                        if form.cleaned_data:
                            form.save(user, author, theme)
                            photo_count += 1

                if photo_count == 0:
                    messages.error(request, "Upload at least one photo.")
                    raise ValidationError("No photo uploaded")

            return redirect('rolca-frontend:upload_confirm')

        except ValidationError:
            pass

    context = {
        'contest_title': contest.title,
        'author_form': author_form,
        'theme_formsets': theme_formsets,
        'show_titles': len(theme_formsets) > 1,

    }

    return render(request, 'frontend/upload.html', context)


confirm_view = TemplateView.as_view(  # pylint: disable=invalid-name
    template_name='frontend/upload_confirm.html')


class SelectContestView(ListView):
    """View for selecting the Salon."""

    template_name = 'frontend/select_contest.html'

    def get_queryset(self):
        """Filter queryset based on start and end date."""
        now = datetime.now()
        return Contest.objects.filter(start_date__lte=now, end_date__gte=now)

    def get(self, request, *args, **kwargs):
        """Redirect to upload if only one contest is active."""
        queryset = self.get_queryset()
        if queryset.count() == 1:
            contest_pk = queryset.first().pk
            return redirect('rolca-frontend:upload', contest_id=contest_pk)

        return super(SelectContestView, self).get(request, *args, **kwargs)


select_contest_view = SelectContestView.as_view()  # pylint: disable=invalid-name


# def list_details(request, contest_id):
#     contest = get_object_or_404(Contest, pk=contest_id)
#     themes = Theme.objects.filter(contest=contest)

#     response = {'users': []}
#     for user in Profile.objects.all():  # pylint: disable=no-member
#         count = Photo.objects.filter(theme__in=themes, user=user).count()
#         if count > 0:
#             response['users'].append({
#                 'name': user.get_short_name,
#                 'school': user.school,
#                 'count': count})

#     response['contest'] = contest
#     return render(request, os.path.join('frontend', 'list_details.html'),
#                   response)

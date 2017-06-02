# -*- coding: utf-8 -*-
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.http.response import JsonResponse
from django.template.loader import render_to_string
from django.views.generic.edit import CreateView

from .forms import UpdateRatingForm
from .models import Rating


class UpdateRatingView(CreateView):
    model = Rating
    form_class = UpdateRatingForm
    template_name = 'rating_stars/rating.html'

    def get_form_kwargs(self):
        kwargs = {
            'initial': self.get_initial(),
            'prefix': self.get_prefix(),
        }
        if self.request.method in ('POST', 'PUT'):
            kwargs.update({
                'data': self.request.POST,
                'files': self.request.FILES,
            })
        return kwargs

    def form_invalid(self, form):
        ctype_id = form.cleaned_data['content_type']
        ctype = ContentType.objects.get(id=ctype_id)
        obj_id = form.cleaned_data['object_id']
        user_id = form.cleaned_data['user_id']

        if not Rating.objects.filter(content_type=ctype, object_id=obj_id).exists():
            data = {
                'html': render_to_string(
                    'rating_stars/rating.html',
                    {
                        'form': form,
                        'object': ctype.model_class().objects.get(id=obj_id),
                        'vote_user_id': user_id,
                        'vote_amount': 0,
                        'vote_average': 0
                    },
                    request=self.request
                )
            }
        else:
            self.object = Rating.objects.get(content_type=ctype, object_id=obj_id)

            data = {}
            if self.request.is_ajax():
                data = {
                    'html': render_to_string(
                        'rating_stars/rating.html',
                        {
                            'form': form,
                            'object': ctype.model_class().objects.get(id=obj_id),
                            'vote_user_id': user_id,
                            'vote_amount': self.object.votes,
                            'vote_average': self.object.average
                        },
                        request=self.request
                    )
                }
        return JsonResponse(data)

    def form_valid(self, form):
        ctype_id = form.cleaned_data['content_type']
        ctype = ContentType.objects.get(id=ctype_id)
        obj_id = form.cleaned_data['object_id']
        user_id = form.cleaned_data['user_id']
        user = User.objects.get(id=user_id)

        self.object, created_at = Rating.objects.get_or_create(
            content_type=ctype, object_id=obj_id
        )

        self.object.user.add(user)
        self.object.votes = self.object.votes + 1
        self.object.total = self.object.total + form.cleaned_data['rating']
        self.object.average = self.object.total / float(self.object.votes)
        self.object.save()

        data = {}
        if self.request.is_ajax():
            data = {
                'html': render_to_string(
                    'rating_stars/rating.html',
                    {
                        'form': form,
                        'object': ctype.model_class().objects.get(id=obj_id),
                        'vote_user_id': user_id,
                        'vote_amount': self.object.votes,
                        'vote_average': self.object.average
                    },
                    request=self.request
                )
            }
        return JsonResponse(data)

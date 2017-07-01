from django import forms
from django.contrib.auth.models import Group, Permission, User
from django.contrib.auth import password_validation
from django.utils.text import slugify
from django.utils.translation import ugettext as _
from thorson_wiki.models import *

class ArticleUpdateForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):

        super(ArticleUpdateForm, self).__init__(*args, **kwargs)

        users = User.objects.all()
        groups = Group.objects.all()

        user_choices = [(user.username, user) for user in users]
        group_choices = [(group.name, group) for group in groups]

        choices = [
            (_("Groups"), group_choices),
            (_("Users"), user_choices),
        ]

        self.fields['read_permissions'] = forms.MultipleChoiceField(
            label=_("Read permissions"),
            choices=choices,
            required=False,
            help_text=_("Select users and groups to grant permission" \
                    " to read this article.")
        )

        self.fields['edit_permissions'] = forms.MultipleChoiceField(
            label=_("Edit permissions"),
            choices=choices,
            required=False,
            help_text=_("Select users and groups to grant permission" \
                    " to edit this article.")
        )

    def save(self, commit=True):
        """
        If commit is set to False, then permissions cannot be updated. Be sure
        to call :func:`save_permissions` at some point if commit is set to
        False.
        """

        article = super(ArticleUpdateForm, self).save(commit=commit)

        if commit:
            self.save_permissions(article)

        return article

    def save_permissions(self, article):
        """
        Saves an article's permissions.
        """

        read_permissions = self.cleaned_data['read_permissions']
        read_permission = Permission.objects.get(
            codename='read-article:%s' % article.slug
        )
        for item in read_permissions:
            if isinstance(item, User):
                item.user_permissions.add(read_permission)
            elif isinstance(item, Group):
                item.permissions.add(read_permission)

        edit_permissions = self.cleaned_data['edit_permissions']
        edit_permission = Permission.objects.get(
            codename='edit-article:%s' % article.slug
        )
        for item in read_permissions:
            if isinstance(item, User):
                item.user_permissions.add(edit_permission)
            elif isinstance(item, Group):
                item.permissions.add(edit_permission)

    def clean_title(self):

        title = self.cleaned_data.get('title')

        if self.instance:
            objects = Article.objects.exclude(id=self.instance.id)
        else:
            objects = Article.objects.all()

        if objects.filter(slug=slugify(title)).exists():
            raise forms.ValidationError(
                    _("An article with that name already" \
                            " exists."),
                    code='already_exists'
            )

        return title

    class Meta:

        model = Article
        fields = ['title', 'namespace', 'content', 'public',
                'redirect']

class UserCreateForm(forms.ModelForm):

    error_messages = {
        'password_mismatch': _("The two password fields didn't match."),
    }

    password1 = forms.CharField(label=_("Password"),
            widget=forms.PasswordInput)
    password2 = forms.CharField(label=_("Password confirmation"),
            widget=forms.PasswordInput,
            help_text=_("Enter your password again."))

    def clean_password2(self):

        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')

        if password1 and password2 == password1:
            pass
        else:
            raise forms.ValidationError(
                    self.error_messages['password_mismatch'],
                    code='password_mismatch',
            )

        password_validation.validate_password(
                self.cleaned_data.get('password2')
        )

        return password2

    def save(self, commit=True):

        user = super(UserCreateForm, self).save(commit=commit)
        user.username = self.cleaned_data.get('username')
        user.set_password(self.cleaned_data['password1'])

        if commit:
            user.save()

        return user

    class Meta:
        model = User
        fields = ['username', 'password1', 'password2', 'email']

class UserUpdateForm(forms.ModelForm):

    class Meta:

        model = User
        fields = ['username', 'email']

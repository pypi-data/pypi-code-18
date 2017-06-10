from django import forms
from django.forms import ModelForm
from jobs.models import ClientProfile
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class JobSubmissionForm(forms.Form):
    job_description = forms.CharField(label="Job description", widget=forms.Textarea)

class ProfileForm(ModelForm):
    class Meta:
        model = ClientProfile
        fields = ['phone', 'street', 'city', 'state', 'zip_code']

class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')

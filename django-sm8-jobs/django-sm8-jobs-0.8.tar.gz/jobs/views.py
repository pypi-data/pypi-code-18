import os
from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.core.mail import EmailMessage
from django.contrib.auth.models import User
from django.forms.models import model_to_dict
from django.urls import reverse
from django.db import transaction

import requests
import json

from jobs.models import JobSubmitted, ClientProfile
from jobs.forms import JobSubmissionForm, ProfileForm, CreateUserForm, UserForm

auth = (settings.SERVICEM8_EMAIL, settings.SERVICEM8_PASSWORD)


def add_job_contact(first_name, last_name, email, phone, job_id, auth):
    url = "https://api.servicem8.com/api_1.0/JobContact.json"
    payload = {
        "first":first_name,
        "last":last_name,
        "email":email,
        "phone":phone,
        "job_uuid":job_id,
        "type":"JOB",
        "is_primary_contact":1,
    }
    r = requests.post(url, data=payload, auth=auth)
    return;

@login_required
def submit_job(request):
    if request.method == 'POST':
        form = JobSubmissionForm(request.POST)
        if form.is_valid():
            first_name = "{}".format(request.user.first_name)
            last_name = "{}".format(request.user.last_name)
            email = "{}".format(request.user.email)
            phone = "{}".format(request.user.clientprofile.phone)
            job_addr = "{0}, {1}, {2} {3}".format(request.user.clientprofile.street, request.user.clientprofile.city, request.user.clientprofile.state, request.user.clientprofile.zip_code)
            job_desc = form.cleaned_data['job_description']
            company = request.user.username
            url = "https://api.servicem8.com/api_1.0/Job.json"
            payload = {
                "status":"Quote",
                "job_address":job_addr,
                "job_description":"{}".format(job_desc),
                "company_id":company,
            }
            r = requests.post(url, data=payload, auth=auth)
            job_id = "{}".format(r.headers['x-record-uuid'])
            j = JobSubmitted(job_id=job_id, job_description=job_desc, user=request.user)
            j.save()
            add_job_contact(first_name=first_name, last_name=last_name, email=email, phone=phone, auth=auth, job_id=job_id)
            return HttpResponseRedirect('/')
    else:
        form = JobSubmissionForm()
    return render(request, 'jobs/submit.html', {'form':form})

@login_required
def get_jobs(request):
    jobs = JobSubmitted.objects.filter(user_id=request.user.id)
    return render(request, 'jobs/index.html', {'jobs': jobs})

@login_required
def get_job_detail(request, jobsubmitted_id):
    j = get_object_or_404(JobSubmitted, user_id=request.user.id, pk=jobsubmitted_id)
    url = "https://api.servicem8.com/api_1.0/Job/{}.json".format(j.job_id)
    r = requests.get(url, auth=auth)
    job = r.json()
    return render(request, "jobs/details.html", {'job': job, 'j':j})

@login_required
def get_job_note(request, jobsubmitted_id):
    n = get_object_or_404(JobSubmitted, user_id=request.user.id, pk=jobsubmitted_id)
    url = "https://api.servicem8.com/api_1.0/Note.json"
    r = requests.get(url, auth=auth)
    notes = r.json()
    return render(request, "jobs/notes.html", {'notes': notes, 'n': n})

@login_required
def get_job_attachment(request, jobsubmitted_id):
    a = get_object_or_404(JobSubmitted, user_id=request.user.id, pk=jobsubmitted_id)
    url = "https://api.servicem8.com/api_1.0/Attachment.json"
    r = requests.get(url, auth=auth)
    attachments = r.json()
    return render(request, "jobs/attachments.html", {'attachments': attachments, 'a': a})

@login_required
def edit_profile(request):
    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=request.user)
        profile_form = ProfileForm(request.POST, instance=request.user.clientprofile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return HttpResponseRedirect(reverse('jobs:list'))
    else:
        user_form = UserForm(instance=request.user)
        profile_form = ProfileForm(instance=request.user.clientprofile)
        return render(request, 'jobs/profile.html', {'user_form': user_form, 'profile_form': profile_form})

@login_required
@transaction.atomic
def create_new_user(request):
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('jobs:new-user'))
    else:
        form = CreateUserForm()
        return render(request, 'jobs/create_user.html', {'form': form})

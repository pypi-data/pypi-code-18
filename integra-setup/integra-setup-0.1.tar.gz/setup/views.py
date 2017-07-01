# Author: Partha
# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import pandas as pd, json

from django.shortcuts import render
from django.http import JsonResponse, HttpResponse

from .models import UserCreds

def list_creds(request):
    """
        Desc: Used to list the credentials of Authenticated User 
    """
    if 'list' in request.GET and request.GET['list'] == 'true':
        user = request.user
        creds = UserCreds.objects.filter(user = request.user).values()
        credsDf = pd.DataFrame.from_records(creds)
        return JsonResponse({'results':credsDf.to_dict(orient = 'records')})
    return render(request, "setup/setup_search.html", {})

def add_creds(request):
    """ 
        @app_type
        @cred_type
        @host
        @db
        @port
        @username
        @password
        @status
    """
    if request.method == "POST":
        # Make sure the data creds provided
        if 'app_type' not in request.POST or request.POST['app_type'] == "":
            return JsonResponse({'message': 'Please provide app_type', 'status': 'fail'})
        if 'cred_type' not in request.POST or request.POST['cred_type'] == "":
            return JsonResponse({'message': 'Please provide cred_type', 'status': 'fail'})
        if 'host' not in request.POST or request.POST['host'] == "":
            return JsonResponse({'message': 'Please provide host', 'status': 'fail'})
        if 'db' not in request.POST or request.POST['db'] == "":
            return JsonResponse({'message': 'Please provide db', 'status': 'fail'})
        if 'port' not in request.POST or request.POST['port'] == "":
            return JsonResponse({'message': 'Please provide port', 'status': 'fail'})
        if 'username' not in request.POST or request.POST['username'] == "":
            return JsonResponse({'message': 'Please provide username', 'status': 'fail'})
        if 'password' not in request.POST or request.POST['password'] == "":
            return JsonResponse({'message': 'Please provide password', 'status': 'fail'})
        if 'status' not in request.POST or request.POST['status'] == "":
            return JsonResponse({'message': 'Please provide status', 'status': 'fail'})
        
        # @params
        payload = {
            'app_type' : request.POST['app_type'],
            'cred_type' : request.POST['cred_type'],
            'host' : request.POST['host'],
            'db' : request.POST['db'],
            'port' : request.POST['port'],
            'username' : request.POST['username'],
            'password' : request.POST['password'],
            'status' : request.POST['status'],
            'user' : request.user # Current Login user
        }
        
        # Saving
        cred = UserCreds.objects.create(**payload)

        # Return Success Message
        return JsonResponse({'message': cred.pk.__str__(), 'status': 'success'})
    return render(request, "setup/setup_add_view_edit.html", {})


def edit_creds(request, pk = None):
    """
        @app_type
        @cred_type
        @host
        @db
        @port
        @username
        @password
        @status
    """
    try:
        cred = UserCreds.objects.get(pk = pk)
    except UserCreds.DoesNotExist: 
        return JsonResponse({'message': 'Credentials Not Found', 'status': 'fail'})
    if request.method == "POST":
    # Make sure the creds exists
        if 'app_type' in request.POST and request.POST['app_type'] != "":
            cred.app_type = request.POST['app_type']
        
        if 'cred_type' in request.POST and request.POST['cred_type'] != "":
            cred.cred_type = request.POST['cred_type']
        
        if 'host' in request.POST and request.POST['host'] != "":
            cred.host = request.POST['host']
        
        if 'db' in request.POST and request.POST['db'] != "":
            cred.db = request.POST['db']
        
        if 'port' in request.POST and request.POST['port'] != "":
            cred.port = request.POST['port']
        
        if 'username' in request.POST and request.POST['username'] != "":
            cred.username = request.POST['username']
        
        if 'password' in request.POST and request.POST['password'] != "":
            cred.password = request.POST['password']
        
        if 'status' in request.POST and request.POST['status'] != "":
            cred.status = request.POST['status']
        
        cred.save()
        return JsonResponse({'message':'Credentials Updated Successfully', 'status': 'fail'})
    if 'list' in request.GET and request.GET['list'] == 'true':
        return HttpResponse(json.dumps(cred.__dict__, default = str))
    return render(request, "setup/setup_view_edit.html", {'creds':cred, 'pk':pk})
    
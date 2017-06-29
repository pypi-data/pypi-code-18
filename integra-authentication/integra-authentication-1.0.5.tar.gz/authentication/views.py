# -*- coding: utf-8 -*-
# Author : Partha

from __future__ import unicode_literals

from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http import JsonResponse, HttpResponseRedirect
from django.shortcuts import render


def user_login(request):
    """
        @username
        @password
        Desc: For User login 
    """
    if request.method == "POST":
        # Make sure the credentials supplied
        if 'username' not in request.POST or request.POST['username'] == "":
            return JsonResponse({'message': 'Please Provide the Username and Password', 'status': 'fail'})
        
        # @params
        username = request.POST['username']
        password = request.POST['password']

        # UserCheck
        user = authenticate(username = username, password = password)

        # If user not exists
        if user is None:
            return JsonResponse({'message': 'Invalid User Credentials', 'status':'fail'})
        
        # If user found, login and return success response
        login(request, user)
        return JsonResponse({'message': 'User Logined Successfully', 'status':'success'})
    return render(request, "authentication/login_register.html", {})


def user_register(request):
    """
        @username
        @password
        @first_name
        @email
        Desc: For User login 
    """
    if request.method == "POST":
        # Make sure that the data provided
        if 'username' not in request.POST or request.POST['username'] == "":
            return JsonResponse({'message': 'Please Provide Username', 'status': 'fail'})

        if 'password' not in request.POST or request.POST['password'] == "":
            return JsonResponse({'message': 'Please Provide Password', 'status': 'fail'})

        if 'first_name' not in request.POST or request.POST['first_name'] == "":
            return JsonResponse({'message': 'Please Provide First Name', 'status': 'fail'})

        if 'email' not in request.POST or request.POST['email'] == "":
            return JsonResponse({'message': 'Please Provide email', 'status': 'fail'})
        
        # @params
        username = request.POST['username']
        first_name = request.POST['first_name']
        email = request.POST['email']
        password = request.POST['password']

        # Check the username available or not
        try:
            user = User.objects.get(username = username)
            return JsonResponse({'message': 'Username Already Exists'})
        except User.DoesNotExist:
            pass
        
        # Check for the email uniquness
        try:
            user = User.objects.get(email = email)
            return JsonResponse({'message': 'Email Already Exists'})
        except User.DoesNotExist:
            pass
        
        # Register the user
        user = User()
        user.username = username
        user.email = email
        user.password = make_password(password)
        user.first_name = first_name
        user.save()
        
        #Return Success Message        
        return JsonResponse({'message': 'User Registered Successfully', 'status': 'success'})

    return render(request, "authentication/login_register.html", {})
    

def user_logout(request):
    """
        Desc: For User logout
    """
    logout(request)
    return HttpResponseRedirect('/auth/login/')
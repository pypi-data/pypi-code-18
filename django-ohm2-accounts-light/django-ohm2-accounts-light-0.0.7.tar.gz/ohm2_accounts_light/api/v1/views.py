from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.decorators import authentication_classes, permission_classes, api_view
from ohm2_handlers_light.parsers import get_as_or_get_default
from . import dispatcher



@api_view(['POST'])
@permission_classes((AllowAny,))
def signup(request):
	"""
	Inputs:
		- username (string, required): user's username
		- password (string, required): user's password
		- email (string-email, optional): user's email

	Output:
		- error (json-dict): describes the error (if known) with a code (integer) and a message (string).
		- ret (boolean): true (boolean) if the signup completed succesfully.

	Notes:
		If username is an email, the email parameter will be overriten by username.	
	"""

	keys = (
		("username", "username", ""),
		("password", "password", ""),
		("email", "email", ""),
	)
	res, error = dispatcher.signup(request, get_as_or_get_default(request.data, keys))
	if error:
		return JsonResponse({"error": error.regroup()})
	return JsonResponse(res)


@api_view(['POST'])
@permission_classes((AllowAny,))
def login(request):
	"""
	Inputs:
		- username (string, required): user's username
		- password (string, required): user's password

	Output:
		- error (json-dict): describes the error (if known) with a code (integer) and a message (string).
		- ret (boolean): true (boolean) if the login completed succesfully.

	Notes:
		None
	"""
	keys = (
		("username", "username", ""),
		("password", "password", ""),
	)
	res, error = dispatcher.login(request, get_as_or_get_default(request.data, keys))
	if error:
		return JsonResponse({"error": error.regroup()})
	return JsonResponse(res)


@api_view(['POST'])
@authentication_classes((TokenAuthentication, SessionAuthentication))
@permission_classes((IsAuthenticated,))
def logout(request):
	"""
	Inputs:
		None

	Output:
		- error (json-dict): describes the error (if known) with a code (integer) and a message (string).
		- ret (boolean): true (boolean) if the logout completed succesfully.

	Notes:
		None
	"""
	keys = (
	)
	res, error = dispatcher.logout(request, get_as_or_get_default(request.data, keys))
	if error:
		return JsonResponse({"error": error.regroup()})
	return JsonResponse(res)



@api_view(['POST'])
@permission_classes((AllowAny,))
def signup_and_get_token(request):
	"""
	Inputs:
		- username (string, required): user's username
		- password (string, required): user's password
		- email (string-email, optional): user's email

	Output:
		- error (json-dict): describes the error (if known) with a code (integer) and a message (string).
		- ret (json-dict): 
			- token (string): user's authentication token

	Notes:
		If username is an email, the email parameter will be overriten by username.	
	"""
	keys = (
		("username", "username", ""),
		("password", "password", ""),
		("email", "email", ""),
	)
	res, error = dispatcher.signup(request, get_as_or_get_default(request.data, keys))
	if error:
		return JsonResponse({"error": error.regroup()})

	elif res.get("error") or not res.get("ret"):
		return JsonResponse({"error" : res.get("error")})

	else:
		res, error = dispatcher.create_authtoken(request, get_as_or_get_default(request.data, (("username", "username", ""),)))

			
	if error:
		return JsonResponse({"error": {"code": -1, "message" : "an error occured"}})
	return JsonResponse(res)


@api_view(['POST'])
@permission_classes((AllowAny,))
def login_and_get_token(request):
	"""
	Inputs:
		- username (string, required): user's username
		- password (string, required): user's password

	Output:
		- error (json-dict): describes the error (if known) with a code (integer) and a message (string).
		- ret (json-dict): 
			- token (string): user's authentication token

	Notes:
		None
	"""
	keys = (
		("username", "username", ""),
		("password", "password", ""),
	)
	res, error = dispatcher.login(request, get_as_or_get_default(request.data, keys))
	if error:
		return JsonResponse({"error" : error.regroup()})

	elif res.get("error") or not res.get("ret"):
		return JsonResponse({"error" : res.get("error", {"code": -1, "message" : "an error occured"})})

	else:
		res, error = dispatcher.get_authtoken(request, get_as_or_get_default(request.data, (("username", "username", ""),)))

			
	if error:
		return JsonResponse({"error": error.regroup()})
	return JsonResponse(res)




from ohm2_handlers_light import utils as h_utils
from ohm2_accounts_light.decorators import ohm2_accounts_light_safe_request
from ohm2_accounts_light import utils as ohm2_accounts_light_utils
from ohm2_accounts_light import settings
from . import errors




@ohm2_accounts_light_safe_request
def signup(request, params):
	p = h_utils.cleaned(params, (
							("string", "username", 1),
							("string", "password", 1),
							("string", "email", 0),
						))

	if request.user.is_authenticated():
		return {"error": errors.USER_ALREADY_LOGGED_IN}
	
	elif ohm2_accounts_light_utils.user_exist(username = p["username"]):
		return {"error" : errors.USER_ALREADY_EXIST}

	elif settings.CHECK_PASSWORD_SECURE and not ohm2_accounts_light_utils.is_password_secure(p["password"]):
		return {"error" : errors.THE_PASSWORD_IS_NOT_SECURE}

	elif len(p["email"]) > 0 and not h_utils.is_email_valid(p["email"]):
		return {"error" : errors.INVALID_EMAIL}

	elif not settings.SIGNUPS_ENABLED:
		return {"error" : errors.SIGNUPS_DISABLED}

	else:
		pass


	username, password, email = p["username"], p["password"], p["email"]

	if len(email) == 0 and h_utils.is_email_valid(username):
		email = username

	
	user = ohm2_accounts_light_utils.create_user(username, email, password)
	try:
		ohm2_accounts_light_utils.run_signup_pipeline(request, user, username, email, password)
	except Exception as e:
		ohm2_accounts_light_utils.delete_user(user)
		return {"error" : errors.SIGNUP_PIPELINE_FAILED}
	



	res = {
		"error" : None,
		"ret" : True,
	}
	return res



@ohm2_accounts_light_safe_request
def login(request, params):
	p = h_utils.cleaned(params, (
							("string", "username", 1),
							("string", "password", 1),
						))


	if request.user.is_authenticated():
		return {"error": None, "ret" : True}
	
	else:
		username, password = p["username"], p["password"]

		
	if not settings.ENABLE_EMAIL_LOGIN and h_utils.is_email_valid(username):
		return {"error" : errors.EMAIL_LOGIN_DISABLED}

	elif settings.ENABLE_EMAIL_LOGIN and h_utils.is_email_valid(username) and ohm2_accounts_light_utils.user_exist(email = username) and settings.UNIQUE_USER_EMAILS:
		user = ohm2_accounts_light_utils.get_user(email = username)
		auth_user = ohm2_accounts_light_utils.user_authenticate(user.get_username(), password)
	
	else:

		auth_user = ohm2_accounts_light_utils.user_authenticate(username, password)
		
	
	
	if auth_user is None:
		return {"error" : errors.WRONG_CREDENTIALS}

	else:
		ohm2_accounts_light_utils.run_login_pipeline(request, auth_user)	
	

	res = {
		"error" : None,
		"ret" : True,
	}
	return res



@ohm2_accounts_light_safe_request
def logout(request, params):
	p = h_utils.cleaned(params,	(
						))


	if not request.user.is_authenticated():
		return {"error": None, "ret" : False}
	
	else:
		ohm2_accounts_light_utils.run_logout_pipeline(request)	
	

	res = {
		"error" : None,
		"ret" : True,
	}
	return res


@ohm2_accounts_light_safe_request
def create_authtoken(request, params):
	p = h_utils.cleaned(params,	(
							("string", "username", 1),
						))


	user = ohm2_accounts_light_utils.get_user(username = p["username"])
	token = ohm2_accounts_light_utils.get_or_create_authtoken(user)

	res = {
		"error" : None,
		"ret" : {
			"token" : token.key,
		}
	}
	return res




@ohm2_accounts_light_safe_request
def get_authtoken(request, params):
	p = h_utils.cleaned(params,	(
							("string", "username", 1),
						))


	user = ohm2_accounts_light_utils.get_user(username = p["username"])
	token = ohm2_accounts_light_utils.get_or_create_authtoken(user)

	res = {
		"error" : None,
		"ret" : {
			"token" : token.key,
		}
	}
	return res



@ohm2_accounts_light_safe_request
def send_password_reset_link(request, params):
	p = h_utils.cleaned(params,	(
							("string", "username", 1),
						))


	if request.user.is_authenticated():
		return {"error": None, "ret" : False}

	username = p["username"]

	if h_utils.is_email_valid(username) and settings.UNIQUE_USER_EMAILS:
		user = ohm2_accounts_light_utils.get_or_none_user(email = username)

	else:	
		user = ohm2_accounts_light_utils.get_or_none_user(username = username)
	
	if user is None:
		return {"error": None, "ret" : False}
		
	passwordreset = ohm2_accounts_light_utils.get_or_none_passwordreset(user = user, activation_date = None)
	if passwordreset is None:
		passwordreset = ohm2_accounts_light_utils.create_passwordreset(user)

	
	sent = False
	if passwordreset.send_again() and settings.PASSWORD_RESET_SEND_ENABLE:

		passwordreset, sent = ohm2_accounts_light_utils.send_passwordreset(passwordreset, request)
		


	res = {
		"error" : None,
		"ret" : sent,
	}
	return res









@ohm2_accounts_light_safe_request
def set_password_reset(request, params):
	p = h_utils.cleaned(params,	(
							("string", "username", 1),
							("string", "password", 1),
							("string", "identity", 0),
							("string", "code", 0),
						))


	if request.user.is_authenticated():
		return {"error": None, "ret" : False}

	username, identity, code, password = p["username"], p["identity"], p["code"], p["password"]

	lookup = {}

	if len(identity) > 0:
		lookup["identity"] = identity

	elif len(code) > 0:
		lookup["code__iexact"] = code
	
	else:
		return {"error" : errors.PASSWORD_RESET_IDENTITY_AND_CODE_CANT_BE_BOTH_EMPTY}


	if h_utils.is_email_valid(username) and settings.UNIQUE_USER_EMAILS:
		lookup["user__email"] = username

	else:
		lookup["user__username"] = username
	

	passwordreset = ohm2_accounts_light_utils.get_or_none_passwordreset(**lookup)
	if passwordreset is None:
		return {"error" : errors.PASSWORD_RESET_INVALID}
	
	elif passwordreset.last_sent_date == None:
		return {"error" : errors.PASSWORD_RESET_INVALID}

	elif passwordreset.activation_date != None:
		return {"error" : errors.PASSWORD_RESET_ALREADY_ACTIVATED}

	elif settings.CHECK_PASSWORD_SECURE and not ohm2_accounts_light_utils.is_password_secure(password):
		return {"error" : errors.THE_PASSWORD_IS_NOT_SECURE}

	else:
		passwordreset = ohm2_accounts_light_utils.change_password_with_passwordreset(passwordreset, password)

		
	res = {
		"error" : None,
		"ret" : True,
	}
	return res



@ohm2_accounts_light_safe_request
def update_user_information(request, params):
	p = h_utils.cleaned(params, (						
							("string", "firstname", 0),
							("string", "lastname", 0),
						))

	
	user = ohm2_accounts_light_utils.get_user(username = request.user.get_username())
	
	user = h_utils.db_update(user, first_name = p["firstname"], last_name = p["firstname"])
	
	ret = {
		"error" : None,
		"ret" : True,
	}
	return ret

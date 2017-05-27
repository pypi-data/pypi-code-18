from emtex_common_utils import set_current_user


class GetCurrentUserMiddleware(object):
    def process_request(self, request):
        if request.user.is_authenticated():
            set_current_user(
                user_email=request.user.email
            )


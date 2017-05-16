from dpuser.serializers.user_detail import UserDetailSerializer

def jwt_response_payload_handler(token, user=None, request=None):
    """
    Returns the response data for both the login and refresh views.
    """
    return {
        'token': token,
        'user': UserDetailSerializer(user, context={'request': request}).data
    }

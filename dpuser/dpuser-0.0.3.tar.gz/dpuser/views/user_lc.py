from rest_framework import generics
from dpuser.models.User import User
from dpuser.serializers.user_lc import UserLCSerializer

class UserLCAPIView(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserLCSerializer

from rest_framework import generics
from dpuser.models.User import User
from dpuser.serializers.user_rud import UserRUDSerializer

class UserRUDAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserRUDSerializer

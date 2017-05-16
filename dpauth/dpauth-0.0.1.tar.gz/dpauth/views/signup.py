from rest_framework import generics
from dpuser.models.User import User
from dpauth.serializers.signup import SignupSerializer

class SignupAPIView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = SignupSerializer

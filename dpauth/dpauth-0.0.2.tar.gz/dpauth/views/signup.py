from rest_framework import generics
from rest_framework.permissions import AllowAny
from dpuser.models.User import User
from dpauth.serializers.signup import SignupSerializer

class SignupAPIView(generics.CreateAPIView):
    permission_classes = (AllowAny,)
    queryset = User.objects.all()
    serializer_class = SignupSerializer

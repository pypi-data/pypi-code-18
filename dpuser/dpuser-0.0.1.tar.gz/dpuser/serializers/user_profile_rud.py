from rest_framework import serializers
from dpuser.models.UserProfile import UserProfile

class UserProfileRUDSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ('bio', 'gender', 'dob')

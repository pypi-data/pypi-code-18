from rest_framework import serializers
from dpuser.models.UserProfile import UserProfile

class UserProfileCSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ('bio', 'dob', 'gender',)

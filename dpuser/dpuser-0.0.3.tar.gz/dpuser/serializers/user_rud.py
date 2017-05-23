from rest_framework import serializers
from dpuser.models.User import User
from dpuser.serializers.user_profile_rud import UserProfileRUDSerializer

class UserRUDSerializer(serializers.ModelSerializer):
	profile = UserProfileRUDSerializer()
	class Meta:
		model = User
		fields = ('id', 'email', 'profile')

	def update(self, instance, validated_data):
		profile_data = validated_data.pop('profile')
		instance.email = validated_data['email']
		instance.bio = profile_data['bio']
		instance.gender = profile_data['gender']
		instance.dob = profile_data['dob']
		instance.save()
		return instance

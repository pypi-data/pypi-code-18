from rest_framework import serializers
from dpuser.models.User import User
from dpuser.serializers.user_profile_c import UserProfileCSerializer
from rest_framework_jwt.settings import api_settings


jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER

class SignupSerializer(serializers.ModelSerializer):
	token = serializers.SerializerMethodField()
	profile = UserProfileCSerializer()
	class Meta:
		model = User
		fields = ('email', 'password', 'profile', 'is_active', 'is_staff', 'is_superuser', 'token')
		extra_kwargs = {
				'password': {'write_only': True}
		}

	def get_token(self, instance):
		try:
			payload = jwt_payload_handler(instance)
			token = jwt_encode_handler(payload)
		except:
			token = None
		return token

	def create(self, validated_data):
		profile_data = validated_data.pop('profile')
		user = User(email=validated_data['email'])
		user.set_password(validated_data['password'])
		user.bio = profile_data['bio']
		user.gender = profile_data['gender']
		user.dob = profile_data['dob']
		user.save()
		return user

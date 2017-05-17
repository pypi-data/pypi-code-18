from rest_framework import serializers
from dpuser.models.User import User
from dpuser.serializers.user_profile_c import UserProfileCSerializer

user_detail_url = serializers.HyperlinkedIdentityField(
	view_name='dpuser-urls:user-retrieve-update-delete',
	lookup_field='pk'
	)

class UserLCSerializer(serializers.ModelSerializer):
	url = user_detail_url
	profile = UserProfileCSerializer()
	class Meta:
		model = User
		fields = ('url', 'email', 'password', 'profile', 'is_active', 'is_staff', 'is_superuser')
		extra_kwargs = {
				'password': {'write_only': True}
		}

	def create(self, validated_data):
		profile_data = validated_data.pop('profile')
		user = User(email=validated_data['email'])
		user.set_password(validated_data['password'])
		user.bio = profile_data['bio']
		user.gender = profile_data['gender']
		user.dob = profile_data['dob']
		user.save()
		return user

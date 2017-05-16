from rest_framework import serializers
from dpuser.models.User import User
# from dpuser.serializers.user_profile_create import UserProfileCreateSerializer

user_detail_url = serializers.HyperlinkedIdentityField(
	view_name='dpuser-urls:user-retrieve-update-delete',
	lookup_field='pk'
	)

class UserDetailSerializer(serializers.ModelSerializer):
	url = user_detail_url
	# profile = UserProfileCreateSerializer()
	class Meta:
		model = User
		fields = ('url', 'email', 'password', 'is_active', 'is_staff', 'is_superuser')
		extra_kwargs = {
				'password': {'write_only': True}
		}

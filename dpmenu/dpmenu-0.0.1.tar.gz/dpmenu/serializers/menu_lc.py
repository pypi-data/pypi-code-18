from rest_framework import serializers
from dpmenu.models.Menu import Menu

menu_detail_url = serializers.HyperlinkedIdentityField(
	view_name='dpmenu-urls:menu-rud',
	lookup_field='pk'
	)

class MenuLCChildrenSerializer(serializers.ModelSerializer):
	# url = menu_detail_url
	class Meta:
		model = Menu
		fields = ('id', 'key', 'title', 'displayType', 'parent', 'title', 'section', 'icon', 'children')

class MenuLCSerializer(serializers.ModelSerializer):
	url = menu_detail_url
	children = serializers.SerializerMethodField()
	class Meta:
		model = Menu
		fields = ('url', 'id', 'key', 'title', 'displayType', 'parent', 'title', 'section', 'icon', 'children')

	def get_children(self, obj):
		return MenuLCChildrenSerializer(obj.get_children(), many=True).data

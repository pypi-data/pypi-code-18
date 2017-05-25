from rest_framework import serializers
from dpmenu.models.Menu import Menu

class MenuRUDSerializer(serializers.ModelSerializer):
	class Meta:
		model = Menu
		fields = ('id', 'name')

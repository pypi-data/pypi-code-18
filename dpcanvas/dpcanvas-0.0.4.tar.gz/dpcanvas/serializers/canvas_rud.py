from rest_framework import serializers
from dpcanvas.models.Canvas import Canvas

class CanvasRUDSerializer(serializers.ModelSerializer):
	class Meta:
		model = Canvas
		fields = ('id', 'name')

from rest_framework import serializers
from dpcanvas.models.Canvas import Canvas

canvas_detail_url = serializers.HyperlinkedIdentityField(
	view_name='dpcanvas-urls:canvas-rud',
	lookup_field='pk'
	)

class CanvasLCSerializer(serializers.ModelSerializer):
	url = canvas_detail_url
	user = serializers.ReadOnlyField(source='user.id')
	class Meta:
		model = Canvas
		fields = ('url', 'name', 'summary', 'user')

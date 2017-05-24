from rest_framework import serializers
from dpprogram.models.Program import Program
from dpcanvas.models.Canvas import Canvas
from dpcanvas.serializers.canvas_rud import CanvasRUDSerializer

program_detail_url = serializers.HyperlinkedIdentityField(
	view_name='dpprogram-urls:program-rud',
	lookup_field='pk'
	)

class ProgramLCSerializer(serializers.ModelSerializer):
	url = program_detail_url
	class Meta:
		model = Program
		fields = ('url', 'name', 'summary', 'canvas')

	# def create(self, validated_data):
	# 	program = Program(**validated_data)
	# 	program.save()
	# 	return program

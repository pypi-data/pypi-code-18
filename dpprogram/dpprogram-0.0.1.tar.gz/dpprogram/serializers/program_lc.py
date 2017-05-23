from rest_framework import serializers
from dpprogram.models.Program import Program

program_detail_url = serializers.HyperlinkedIdentityField(
	view_name='dpprogram-urls:program-rud',
	lookup_field='pk'
	)

class ProgramLCSerializer(serializers.ModelSerializer):
	url = program_detail_url
	class Meta:
		model = Program
		fields = ('url', 'name')

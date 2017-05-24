from rest_framework import serializers
from dpprogram.models.Program import Program

class ProgramRUDSerializer(serializers.ModelSerializer):
	class Meta:
		model = Program
		fields = ('id', 'name')

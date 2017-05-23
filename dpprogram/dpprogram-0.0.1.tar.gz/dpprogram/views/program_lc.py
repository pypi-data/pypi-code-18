from rest_framework import generics
from dpprogram.models.Program import Program
from dpprogram.serializers.program_lc import ProgramLCSerializer

class ProgramLCAPIView(generics.ListCreateAPIView):
    queryset = Program.objects.all()
    serializer_class = ProgramLCSerializer

from rest_framework import generics
from dpprogram.models.Program import Program
from dpprogram.serializers.program_rud import ProgramRUDSerializer

class ProgramRUDAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Program.objects.all()
    serializer_class = ProgramRUDSerializer

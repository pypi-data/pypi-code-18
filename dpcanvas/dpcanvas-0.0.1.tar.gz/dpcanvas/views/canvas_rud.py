from rest_framework import generics
from dpcanvas.models.Canvas import Canvas
from dpcanvas.serializers.canvas_rud import CanvasRUDSerializer

class CanvasRUDAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Canvas.objects.all()
    serializer_class = CanvasRUDSerializer

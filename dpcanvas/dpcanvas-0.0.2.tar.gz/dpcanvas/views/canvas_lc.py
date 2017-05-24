from rest_framework import generics
from dpcanvas.models.Canvas import Canvas
from dpcanvas.serializers.canvas_lc import CanvasLCSerializer

class CanvasLCAPIView(generics.ListCreateAPIView):
    queryset = Canvas.objects.all()
    serializer_class = CanvasLCSerializer

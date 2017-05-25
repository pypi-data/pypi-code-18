from rest_framework import generics
from dpmenu.models.Menu import Menu
from dpmenu.serializers.menu_lc import MenuLCSerializer

class MenuLCAPIView(generics.ListCreateAPIView):
    queryset = Menu.objects.filter(parent__isnull=True)
    serializer_class = MenuLCSerializer

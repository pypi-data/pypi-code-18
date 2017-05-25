from rest_framework import generics
from dpmenu.models.Menu import Menu
from dpmenu.serializers.menu_rud import MenuRUDSerializer

class MenuRUDAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Menu.objects.all()
    serializer_class = MenuRUDSerializer

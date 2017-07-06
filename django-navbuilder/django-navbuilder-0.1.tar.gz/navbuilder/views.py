from django.views import generic

from navbuilder.models import Menu


class MenuDetailView(generic.detail.DetailView):
    model = Menu


class MenuListView(generic.list.ListView):
    model = Menu

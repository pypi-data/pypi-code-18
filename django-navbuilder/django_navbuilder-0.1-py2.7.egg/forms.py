from django import forms


from navbuilder.models import Menu, MenuItem


class MenuAdminForm(forms.ModelForm):
    class Meta:
        model = Menu
        fields = ["title", "slug"]


class MenuItemAdminForm(forms.ModelForm):
    class Meta:
        model = MenuItem
        fields = [
            "title", "slug", "position", "menu", "parent", "target",
            "link_content_type", "link_object_id"
        ]

from django import template
from django.contrib.contenttypes.models import ContentType

from navbuilder.models import Menu, MenuItem

register = template.Library()


# These wrappers emulate the queryset API expected by templates.
# todo: use metaclasses
class Wrapper(object):

    def __init__(self, context):
        self._context = context
        self._menuitems = []
        self._submenuitems = []
        self._link = None

    def __getattr__(self, name):
        try:
            return super(Wrapper, self).__getattr__(name)
        except AttributeError:
            return getattr(self._context, name)

    @property
    def menuitems(self):
        return {"all": self._menuitems}

    @property
    def submenuitems(self):
        return {"all": self._submenuitems}

    @property
    def link(self):
        return self._link


class MenuWrapper(Wrapper):
    __class__ = Menu


class MenuItemWrapper(Wrapper):
    __class__ = MenuItem


@register.inclusion_tag(
    "navbuilder/inclusion_tags/menu_detail.html", takes_context=True
)
def render_menu(context, slug):
    try:
        menu = Menu.objects.get(slug=slug)
    except Menu.DoesNotExist:
        return context

    # Reduce the number of queries by using select_related and a number of
    # dictionaries. We present the template with a single structure.
    # Retrieving generic foreign keys is expensive, so the first part of this
    # algorithm fetches them efficiently. The second part builds the menuitem
    # tree.
    menuitems = []
    for obj in MenuItem.objects.filter(root_menu=menu).select_related(
        "parent"
    ):
        menuitems.append(MenuItemWrapper(obj))

    # Key is content type id, value is link id
    map_ct_links = {}

    # Key one is content type id, key two is link id, value is a list of
    # menuitems.
    map_two_deep = {}

    # Populate the dictionaries
    for menuitem in menuitems:
        ct_id = menuitem.link_content_type_id
        link_id = menuitem.link_object_id
        if not link_id:
            continue

        # map_ct_links
        if ct_id not in map_ct_links:
            map_ct_links[ct_id] = []
        map_ct_links[ct_id].append(link_id)

        # map_two_deep
        if ct_id not in map_two_deep:
            map_two_deep[ct_id] = {}
        if link_id not in map_two_deep[ct_id]:
            map_two_deep[ct_id][link_id] = []
        map_two_deep[ct_id][link_id].append(menuitem)

    # Pre-lookup the content types
    content_types = {}
    for ct in ContentType.objects.filter(id__in=map_ct_links.keys()):
        content_types[ct.id] = ct

    # Set the link objects on the menuitems
    for ct_id, ids in map_ct_links.items():
        for obj in content_types[ct_id].model_class().objects.filter(id__in=ids):
            for menuitem in map_two_deep[ct_id][obj.id]:
                menuitem._link = obj

    # Build the nodes dictionary
    nodes = {}
    for obj in menuitems:
        nodes[obj.id] = obj

    # Create the tree and set the parent-child relationships. Menu can now be
    # wrapped.
    menu = MenuWrapper(menu)
    for obj in menuitems:
        if obj.parent is not None:
            parent_id = obj.parent.id
        else:
            parent_id = None
        node = nodes[obj.id]

        if parent_id is None:
            menu._menuitems.append(node)
        else:
            # The "if" statement is to account for bad data
            if parent_id in nodes:
                nodes[parent_id]._submenuitems.append(node)

    context["object"] = menu
    return context


@register.inclusion_tag(
    "navbuilder/inclusion_tags/menuitem_detail.html", takes_context=True
)
def render_menuitem(context, obj):
    context["object"] = obj
    return context


@register.inclusion_tag(
    "navbuilder/inclusion_tags/breadcrumbs.html", takes_context=True
)
def navbuilder_breadcrumbs(context, slug):
    """
    Render the breadcrumbs, based on the current object. Prefer using the
    structure of the menu designated by slug, but use any menu available.
    Typical use case for this would be if the main menu has an about/terms
    page, but it's mirrored in the footer menu in a much flatter layout. We
    prefer the main menu structure. This also allows us to construct
    breadcrumbs for items that don't show up in page menus at all.
    """
    di = {}
    di["navbuilder_breadcrumbs"] = []
    if "object" not in context:
        return context

    def get_menuitems(item):
        if item.parent:
            struct = get_menuitems(item.parent)
            struct.append(item)
            return struct
        return [item]

    content_type = ContentType.objects.get_for_model(context["object"])
    crumb_sets = []
    for item in MenuItem.objects.filter(
            link_content_type__pk=content_type.id,
            link_object_id = context["object"].id):

        crumb_sets.append(get_menuitems(item))

    for crumb_set in crumb_sets:
        menu = crumb_set[0].menu
        if menu and menu.slug == slug:
            di["navbuilder_breadcrumbs"] = crumb_set

    if not di["navbuilder_breadcrumbs"]:
        if crumb_sets:
            di["navbuilder_breadcrumbs"] = crumb_sets[0]
        else:
            di["navbuilder_breadcrumbs"] = []

    context.update(di)
    return context

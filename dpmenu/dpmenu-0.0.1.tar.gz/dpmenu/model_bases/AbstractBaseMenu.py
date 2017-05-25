from django.db import models
from django.utils.translation import ugettext_lazy as _
from mptt.models import MPTTModel, TreeForeignKey

TITLE = 'Title'
ICON = 'Icon'
ICONTITLE = 'IconTitle'
BUTTON = 'Button'
ICONBADGE = 'IconBadge'
ICONTITLEBADGE = 'IconTitleBadge'

DISPLAY_TYPE_CHOICES = (
	(TITLE, 'Title'),
	(ICON, 'Icon'),
	(ICONTITLE, 'IconTitle'),
	(BUTTON, 'Button'),
	(ICONBADGE, 'IconBadge'),
	(ICONTITLEBADGE, 'IconTitleBadge'),
	)

FLAT = 'Flat'
SUBMENU = 'Submenu'

NESTING_TYPE_CHOICES = (
	(FLAT, 'Flat'),
	(SUBMENU, 'Submenu'),
	)

class AbstractBaseMenu(MPTTModel):
	createdAt = models.DateTimeField(auto_now_add=True)
	updatedAt = models.DateTimeField(auto_now=True)
	parent = TreeForeignKey('self', null=True, blank=True, related_name='children', db_index=True)
	title = models.TextField(max_length=500, null=True, blank=True)
	section = models.CharField(max_length=240, null=True, blank=True)
	key = models.CharField(max_length=240, null=True, blank=True)
	icon = models.CharField(max_length=240,null=True,blank=True)
	displayType = models.CharField(
		max_length=50,
		choices=DISPLAY_TYPE_CHOICES,
		null=True,
		blank=True
		)

	class MPTTMeta:
		order_insertion_by = ['title']

	def __str__(self):
		return self.title

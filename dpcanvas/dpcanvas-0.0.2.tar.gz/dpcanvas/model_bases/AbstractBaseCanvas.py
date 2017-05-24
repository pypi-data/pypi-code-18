from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.conf import settings
from dpcanvas.managers.CanvasManager import CanvasManager

class AbstractBaseCanvas(models.Model):
	user = models.ForeignKey(
		settings.AUTH_USER_MODEL,
		on_delete=models.CASCADE,
		related_name="canvas",
        verbose_name=_("user"))
	name = models.TextField(max_length=500)
	summary = models.TextField(max_length=500, null=True, blank=True)
	objects = CanvasManager()

	def __str__(self):
		return self.name

	class Meta:
		abstract = True

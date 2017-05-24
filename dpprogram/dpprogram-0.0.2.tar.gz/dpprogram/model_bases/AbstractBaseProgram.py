from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.conf import settings
from dpcanvas.models import Canvas
from dpprogram.managers.ProgramManager import ProgramManager

class AbstractBaseProgram(models.Model):
	createdAt = models.DateTimeField(auto_now_add=True)
	updatedAt = models.DateTimeField(auto_now=True)
	canvas = models.ForeignKey(
		Canvas,
		on_delete=models.CASCADE,
		related_name="program",
        verbose_name=_("canvas"))
	name = models.TextField(max_length=500, null=True, blank=True)
	summary = models.TextField(max_length=500, null=True, blank=True)
	objects = ProgramManager()


	def __str__(self):
		return self.name

	class Meta:
		abstract = True

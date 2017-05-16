from django.db import models
from django.conf import settings
from django.db.models.signals import post_save
from django.utils.translation import ugettext_lazy as _
from django.dispatch import receiver
from dpuser.managers.UserProfileManager import UserProfileManager

GENDER_CHOICES = (
('M', 'Male'),
('F', 'Female'),
('P', 'Prefer not to answer'),
)

class UserProfile(models.Model):
	user = models.OneToOneField(
		settings.AUTH_USER_MODEL,
		on_delete=models.CASCADE,
		related_name="profile",
        verbose_name=_("user"))
	bio = models.TextField(max_length=500, null=True, blank=True)
	gender = models.CharField(max_length=1,
                              choices=GENDER_CHOICES,
							  null=True,
							  blank=True)
	dob = models.DateField(null=True, blank=True)
	objects = UserProfileManager()

	def __str__(self):
		return self.user.email

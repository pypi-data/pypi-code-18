from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.sites.models import Site
from django.template.defaultfilters import slugify
from django_countries.fields import CountryField

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=CASADE)
    other_name = models.CharField(
        max_length=200,
        blank=True,
        null=True,
        help_text=""
    )
    about = models.CharField(
        max_length=200,
        blank=True,
        null=True,
        help_text=""
    )
    employer = models.CharField(
		max_length=200, 
		blank=True, 
		null=True,
		help_text=""
	)
    position = models.CharField(
		max_length=200, 
		blank=True, 
		null=True,
		help_text=""
	)
    gender = models.CharField(
		max_length=200, 
		blank=True, 
		null=True,
		help_text=""
	)
    ethnicity = models.CharField(
		max_length=200, 
		blank=True, 
		null=True,
		help_text=""
	)
    facebook = models.CharField(
		max_length=200, 
		blank=True, 
		null=True,
		help_text=""
	)
    twitter = models.CharField(
		max_length=200, 
		blank=True, 
		null=True,
		help_text=""
	)
    linkedin = models.CharField(
		max_length=200, 
		blank=True, 
		null=True,
		help_text=""
	)
    blog = models.CharField(
		max_length=200, 
		blank=True, 
		null=True,
		help_text=""
	)
    image = models.CharField(
		max_length=200, 
		blank=True, 
		null=True,
		help_text=""
	)
    cover_image = models.CharField(
		max_length=200, 
		blank=True, 
		null=True,
		help_text=""
	)
    
    def __str__(self):
        return self.user.first_name + ' ' + self.user.last_name
from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class JobSubmitted(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
    )
    job_id = models.CharField(max_length=120)
    job_description = models.TextField()
    date_created = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Job submitted"
        verbose_name_plural = "Jobs submitted"

    def __str__(self):
        return self.job_id

class ClientProfile(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
    )
    phone = models.CharField(max_length=20, blank=True)
    street = models.CharField(max_length=120, blank=True)
    city = models.CharField(max_length=80, blank=True)
    state = models.CharField(max_length=80, blank=True)
    zip_code = models.CharField(max_length=80, blank=True)
    date_created = models.DateTimeField(auto_now_add=True)
    is_approved = models.BooleanField(default=False)

    def __str__(self):
        return "{0}, {1}, {2} {3}".format(self.street, self.city, self.state, self.zip_code)

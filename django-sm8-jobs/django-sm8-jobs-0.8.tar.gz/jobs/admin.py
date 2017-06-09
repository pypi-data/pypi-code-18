from django.contrib import admin
from jobs.models import JobSubmitted, ClientProfile
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User

@admin.register(JobSubmitted, ClientProfile)
class JobAdmin(admin.ModelAdmin):
    pass

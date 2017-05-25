from django.contrib import admin
from slothTw.models import *
# Register your models here.
class CourseAdmin(admin.ModelAdmin):
    list_display = ('name', 'ctype', 'dept', 'teacher')
    search_fields = ('name', 'ctype', 'dept', 'teacher')

admin.site.register(Course, CourseAdmin)
admin.site.register(Comment)
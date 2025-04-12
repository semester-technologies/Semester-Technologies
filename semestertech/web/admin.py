from django.contrib import admin
from .models import Student, Course, UserProfile

admin.site.register([Student, Course, UserProfile])

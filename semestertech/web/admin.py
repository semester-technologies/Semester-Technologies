from django.contrib import admin
from .models import Student, Course, UserProfile, Service, ServiceRequest, SavedCourse, CourseRegistration, Payment

admin.site.register([Student, Course, UserProfile, Service, ServiceRequest, SavedCourse, CourseRegistration, Payment])

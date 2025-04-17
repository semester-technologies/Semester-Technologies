from django.db import models
from django.contrib.auth.models import User

class Course(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=10, unique=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    duration = models.CharField(max_length=200)

    def __str__(self):
        return f"{self.code} - {self.name}"

class Student(models.Model):
    full_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15)
    registered_courses = models.ManyToManyField(Course)

    def __str__(self):
        return self.full_name


class Service(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    duration = models.CharField(max_length=200)
    
    def __str__(self):
        return self.name

class SavedCourse(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    saved_date = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('user', 'course')
    
    def __str__(self):
        return f"{self.user.username} - {self.course.name}"

class CourseRegistration(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending Payment'),
        ('completed', 'Completed'),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    registration_date = models.DateTimeField(auto_now_add=True)
    payment_status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    payment_date = models.DateTimeField(null=True, blank=True)
    
    def __str__(self):
        return f"{self.user.username} - {self.course.name}"

class ServiceRequest(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending Payment'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    request_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    payment_date = models.DateTimeField(null=True, blank=True)
    completion_date = models.DateTimeField(null=True, blank=True)
    
    def __str__(self):
        return f"{self.user.username} - {self.service.name}"

class Payment(models.Model):
    TYPE_CHOICES = (
        ('course', 'Course Payment'),
        ('service', 'Service Payment'),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_date = models.DateTimeField(auto_now_add=True)
    payment_type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    course = models.ForeignKey(Course, null=True, blank=True, on_delete=models.SET_NULL)
    service = models.ForeignKey(Service, null=True, blank=True, on_delete=models.SET_NULL)
    transaction_id = models.CharField(max_length=100, unique=True)
    
    def __str__(self):
        return f"{self.user.username} - {self.amount} - {self.payment_date}"

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=20)
    is_first_login = models.BooleanField(default=True)
    
    def __str__(self):
        return self.user.username
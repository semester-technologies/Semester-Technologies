from django.db import models
from django.contrib.auth.models import User

# class Course(models.Model):
#     CATEGORY_CHOICES = (
#         ('software_development', 'Software Development'),
#         ('data_science', 'Data Science'),
#         ('cyber_security', 'Cyber Security'),
#         ('robotics', 'Robotics'),
#         ('management', 'Management'),
#     )

#     name = models.CharField(max_length=100)
#     code = models.CharField(max_length=10, blank=True, null=True)
#     price = models.DecimalField(max_digits=10, decimal_places=2)
#     description = models.TextField()
#     duration = models.CharField(max_length=200)
#     category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default='software_development')
#     image = models.ImageField(upload_to='course_images/', blank=True, null=True)  # <<== added here


#     def __str__(self):
#         return f"{self.code} - {self.name}"


import datetime  # <== if you need for start_date default

class Course(models.Model):
    CATEGORY_CHOICES = (
        ('software_development', 'Software Development'),
        ('data_science', 'Data Science'),
        ('cyber_security', 'Cyber Security'),
        ('robotics', 'Robotics'),
        ('management', 'Management'),
    )

    name = models.CharField(max_length=100)
    code = models.CharField(max_length=10, blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField(help_text="Brief description of the course.")
    duration = models.CharField(max_length=200, help_text="E.g., '6 weeks', '3 months'")
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default='software_development')
    image1 = models.ImageField(upload_to='course_images/', blank=True, null=True)
    image2 = models.ImageField(upload_to='course_images/', blank=True, null=True)
    image3 = models.ImageField(upload_to='course_images/', blank=True, null=True)
    image4 = models.ImageField(upload_to='course_images/', blank=True, null=True)


    start_date = models.DateField(help_text="Course official start date.", default=datetime.date.today)
    hour_commitment = models.IntegerField(help_text="Estimated total hours required to complete the course.", default=40)
    course_outline = models.TextField(help_text="Detailed breakdown of what the course covers.", default='Course outline coming soon.')
    program_requirements = models.TextField(help_text="Requirements to enroll for the course (skills, prior knowledge, etc.).", default='No special requirements.')
    why_take_this_course = models.TextField(help_text="Persuasive reasons why someone should take this course.", default='Details coming soon.')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    is_active = models.BooleanField(default=True, help_text="Uncheck to deactivate this course.")


    def __str__(self):
        return f"{self.code or ''} {self.name}"

    class Meta:
        ordering = ['-created_at']



class Curriculum(models.Model):
    course = models.ForeignKey(Course, related_name="curriculum", on_delete=models.CASCADE)
    week_number = models.PositiveIntegerField()
    title = models.CharField(max_length=255, help_text="Title for this week e.g., 'Introduction to Python'")
    content = models.TextField(help_text="Detailed content for this week.")

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['week_number']

    def __str__(self):
        return f"Week {self.week_number}: {self.title}"






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
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    duration = models.CharField(max_length=200, null=True, blank=True)
    
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
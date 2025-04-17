from django.shortcuts import render, redirect
from .models import Student, Course
from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .models import UserProfile
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.utils import timezone
from django.urls import reverse
from django.http import HttpResponse
from django.conf import settings
from .models import Course, Service, CourseRegistration, ServiceRequest, SavedCourse
from collections import defaultdict


# Create your views here.

def index(request):
    return render(request, 'web/index.html')

def about(request):
    return render(request, 'web/about.html')

def contact(request):
    return render(request, 'web/contact.html')

def services(request):
    return render(request, 'web/services.html')

def portfolio(request):
    return render(request, 'web/portfolio.html')

def career(request):
    return render(request, 'web/career.html')


def register_user(request):
    if request.method == 'POST':
        print("POST received")
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        if password1 != password2:
            messages.error(request, 'Passwords do not match.')
            return redirect('web:register_user')

        if User.objects.filter(username=email).exists():
            messages.error(request, 'User already exists.')
            return redirect('web:register_user')

        user = User.objects.create_user(
            username=email,
            email=email,
            password=password1,
            first_name=first_name,
            last_name=last_name
        )
        user.save()

        UserProfile.objects.create(user=user, phone=phone)
        messages.success(request, 'Registration successful. Please log in.')
        return redirect('web:login_user')
    else:
        print("GET request - rendering form")
        return render(request, 'web/register.html')


def login_user(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = authenticate(request, username=email, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, 'Logged in successfully.')
            return redirect('web:dashboard')
        else:
            messages.error(request, 'Invalid credentials')
            return redirect('web:login_user')

    return render(request, 'web/login.html')



def logout_user(request):
    logout(request) 
    return redirect('web:login_user')  

@login_required
def dashboard(request):
    user_profile = request.user.userprofile
    # is_first_login = user_profile.is_first_login
    
    # if is_first_login:
    #     user_profile.is_first_login = False
    #     user_profile.save()
    #     return render(request, 'web/dashboard_first_login.html')
    # else:
    registered_courses = CourseRegistration.objects.filter(user=request.user, payment_status='completed')
    requested_services = ServiceRequest.objects.filter(user=request.user)
    saved_courses = SavedCourse.objects.filter(user=request.user)
    
    context = {
        'registered_courses': registered_courses,
        'requested_services': requested_services,
        'saved_courses': saved_courses
    }
    return render(request, 'web/dashboard.html', context)


@login_required
def courses_list(request):
    categories = [
        {'id': 'software_development', 'name': 'Software Development', 'description': 'At Semester Tech, you will learn how to create a dynamic,responsive and user friendly website and applications. We have tech expert that will teach and guide you on how to design a stunning website, build a robust web application also to develop a mobile and desktop apps.', 'image': 'assets/imgs/service-icon-1.svg'},
        {'id': 'data_science', 'name': 'Data Science', 'description': 'Semester Integrated Technologies, you will learn how to analyze, visualize, and derive insights from data to drive decision-making and innovation then also to Unlock the power of data with our comprehensive Data Science programs.', 'image': 'assets/imgs/service-icon-2.svg'},
        {'id': 'cyber_security', 'name': 'Cyber Security', 'description': 'At Semester Integrated Technologies, we provide in-depth training on network security, encryption, risk management, and cybersecurity frameworks also our programs prepare you for roles such as Security Analyst, Network Security Engineer, penetration tester, ethical hacker and Cyber Risk Consultant.', 'image': 'assets/imgs/service-icon-3.svg'},
        {'id': 'robotics', 'name': 'Robotics', 'description': 'At Semester Integrated Technologies, we shall equip you with the skills to design, build, and program intelligent robotic systems. Also train you mechanical design, embedded programming, AI integration and automation and prepare you for careers in industrial automation, healthcare robotics, drone technology, and AI-driven robotics solutions.', 'image': 'assets/imgs/service-icon-4.svg'},
        {'id': 'management', 'name': 'Management', 'description': 'At Semester Integrated Technologies,you will take your organization to the level with our comprehensive management program from elevating your Online presence and crafting user-centered digital experiences, to developing successful products and delivering Projects efficiently, our expert-led training equip you with the skills to drive business growth and achieve success.', 'image': 'assets/imgs/service-icon-5.svg'},
    ]

    # Group courses by category
    courses = Course.objects.all()
    courses_by_category = defaultdict(list)
    for course in courses:
        courses_by_category[course.category].append(course)

    context = {
        'categories': categories,
        'courses_by_category': courses_by_category,
    }
    return render(request, 'web/courses_list.html', context)



@login_required
def course_detail(request, course_id):
    course = Course.objects.get(pk=course_id)
    is_saved = SavedCourse.objects.filter(user=request.user, course=course).exists()
    is_registered = CourseRegistration.objects.filter(user=request.user, course=course, payment_status='completed').exists()
    
    context = {
        'course': course,
        'is_saved': is_saved,
        'is_registered': is_registered
    }
    return render(request, 'web/course_detail.html', context)


@login_required
def download_brochure(request, course_id):
    course = Course.objects.get(pk=course_id)
    # This is placeholder code - in a real application, you would generate
    # or retrieve a PDF file and return it as a download
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{course.code}_brochure.pdf"'
    
    # Here you would add the actual PDF content
    # For now, let's return a simple message
    response.write(f"This is the brochure for {course.name} ({course.code})")
    
    return response


@login_required
def services_list(request):
    services = Service.objects.all()
    context = {
        'services': services
    }
    return render(request, 'web/services_list.html', context)

@login_required
def service_detail(request, service_id):
    service = Service.objects.get(pk=service_id)
    pending_request = ServiceRequest.objects.filter(
        user=request.user,
        service=service,
        status='pending'
    ).first()
    
    context = {
        'service': service,
        'pending_request': pending_request
    }
    return render(request, 'web/service_detail.html', context)

@login_required
def request_service(request, service_id):
    service = Service.objects.get(pk=service_id)
    
    service_request, created = ServiceRequest.objects.get_or_create(
        user=request.user,
        service=service,
        status='pending'
    )
    
    context = {
        'service': service,
        'service_request': service_request,
    }
    return render(request, 'web/service_payment_page.html', context)

def send_course_confirmation_email(user, course):
    # Send receipt email
    receipt_subject = f"Receipt for your course registration: {course.name}"
    receipt_message = f"""
    Dear {user.first_name} {user.last_name},
    
    Thank you for registering for {course.name}. This email serves as your receipt.
    
    Course: {course.name} ({course.code})
    Price: ${course.price}
    Duration: {course.duration}
    Registration Date: {timezone.now().strftime('%Y-%m-%d %H:%M')}
    
    If you have any questions, please contact our support team.
    
    Thank you,
    Course Registration Team
    """
    send_mail(
        receipt_subject,
        receipt_message,
        settings.DEFAULT_FROM_EMAIL,
        [user.email],
        fail_silently=False,
    )
    
    # Send welcome email from CEO
    welcome_subject = f"Welcome to {course.name}!"
    welcome_message = f"""
    Dear {user.first_name} {user.last_name},
    
    Welcome to {course.name}! We're excited to have you join us on this learning journey.
    
    Your course materials will be available soon. In the meantime, join our WhatsApp community for updates and to connect with fellow students:
    
    [WhatsApp Community Link]
    
    Looking forward to seeing your progress!
    
    Best regards,
    [CEO Name]
    CEO
    """
    send_mail(
        welcome_subject,
        welcome_message,
        settings.CEO_EMAIL,  # You'll need to define this in settings
        [user.email],
        fail_silently=False,
    )

def send_service_confirmation_email(user, service):
    receipt_subject = f"Receipt for your service request: {service.name}"
    receipt_message = f"""
    Dear {user.first_name} {user.last_name},
    
    Thank you for requesting {service.name}. This email serves as your receipt.
    
    Service: {service.name}
    Price: ${service.price}
    Estimated Duration: {service.duration}
    Request Date: {timezone.now().strftime('%Y-%m-%d %H:%M')}
    
    You can track the progress of your service request from your dashboard.
    
    If you have any questions, please contact our support team.
    
    Thank you,
    Service Team
    """
    send_mail(
        receipt_subject,
        receipt_message,
        settings.DEFAULT_FROM_EMAIL,
        [user.email],
        fail_silently=False,
    )

@login_required
def payment_success(request):
    return render(request, 'web/payment_success.html')






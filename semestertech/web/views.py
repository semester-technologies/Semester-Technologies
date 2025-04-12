from django.shortcuts import render, redirect
from .models import Student, Course
from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib import messages
from .models import UserProfile


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
            return redirect('register_user')

        if User.objects.filter(username=email).exists():
            messages.error(request, 'User already exists.')
            return redirect('register_user')

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
        return redirect('login_user')
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
            return redirect('dashboard')
        else:
            messages.error(request, 'Invalid credentials')
            return redirect('login_user')

    return render(request, 'web/login.html')



def logout_user(request):
    pass

def dashboard(request):
    return render(request, 'web/dashboard.html')



def register_student(request):
    courses = Course.objects.all()

    if request.method == "POST":
        full_name = request.POST.get('full_name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        selected_courses = request.POST.getlist('courses')

        if Student.objects.filter(email=email).exists():
            messages.error(request, "A student with this email already exists.")
            return redirect('register_student')

        student = Student.objects.create(
            full_name=full_name,
            email=email,
            phone=phone
        )
        student.registered_courses.set(selected_courses)
        student.save()

        messages.success(request, "Registration successful!")
        return redirect('register_student')

    return render(request, 'web/register_student.html', {'courses': courses})



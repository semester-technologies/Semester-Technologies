from django.shortcuts import render

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


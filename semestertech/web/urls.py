from django.urls import path
from web.views import contact, dashboard, index,career, login_user, logout_user, portfolio, register_user,services,about, courses_list, course_detail, download_brochure, services_list, service_detail, request_service, payment_success
from django.contrib.sitemaps.views import sitemap
from web.sitemaps import StaticViewSitemap

app_name = 'web'

sitemaps = {
    'static': StaticViewSitemap,
}

urlpatterns = [
    path('', index, name='index'),
    path('contact/',contact,name='contact'),
    path('portfolio/', portfolio, name='portfolio'),
    path('career/', career, name='career'),
    path('services/', services, name='services'),
    path('about/', about, name='about'),

    path('register/', register_user, name='register_user'),
    path('login/', login_user, name='login_user'),
    path('logout/', logout_user, name='logout_user'),
    path('dashboard/', dashboard, name='dashboard'),

    path('courses/', courses_list, name='courses_list'),
    path('course/<int:course_id>/', course_detail, name='course_detail'),
    path('course/<int:course_id>/brochure/', download_brochure, name='download_brochure'),
    
    path('tech-services/', services_list, name='services_list'),
    path('service/<int:service_id>/', service_detail, name='service_detail'),
    path('service/<int:service_id>/request/', request_service, name='request_service'),

    path('payment-success/', payment_success, name='payment_success'),


    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='sitemap'),

]

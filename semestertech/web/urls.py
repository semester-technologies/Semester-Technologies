from django.urls import path

from web.views import contact, dashboard, index,career, login_user, logout_user, portfolio, register_user,services,about, register_student
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


    # path('register/', register_student, name='register_student'),

    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='sitemap'),

]
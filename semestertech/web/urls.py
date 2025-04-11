from django.urls import path

from web.views import contact, index,career, portfolio,services,about
from django.contrib.sitemaps.views import sitemap
from web.sitemaps import StaticViewSitemap

app_name = 'web'

sitemaps = {
    'static': StaticViewSitemap,
}

urlpatterns = [
    path('', index,name='index'),
    path('contact/',contact,name='contact'),
    path('portfolio/', portfolio, name='portfolio'),
    path('career/', career, name='career'),
    path('services/', services, name='services'),
    path('about/', about, name='about'),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='sitemap'),

]
# sitemaps.py
from django.contrib.sitemaps import Sitemap
from django.urls import reverse

class StaticViewSitemap(Sitemap):
    priority = 0.5
    changefreq = 'monthly'

    def items(self):
        return ['web:index', 'web:about', 'web:contact', 'web:portfolio', 'web:career', 'web:services']

    def location(self, item):
        return reverse(item)

from django.contrib import admin

from webapp.models import Product, Review

admin.site.register(Product, Review)

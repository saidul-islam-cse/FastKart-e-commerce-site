from django.contrib import admin

# Register your models here.
from .models import Category, Product , ProductImage, Review

admin.site.register((Category, Product, ProductImage, Review))
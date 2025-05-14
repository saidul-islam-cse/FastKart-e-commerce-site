from django.shortcuts import render
from django.db.models import Count
from .import models
# Create your views here.
def home(request):
    products = models.Product.objects.all()
    categories = models.Category.objects.annotate(product_count=Count("products"))

    context = {"products" : products, "categories" : categories}

    return render(request, "products/home.html", context)
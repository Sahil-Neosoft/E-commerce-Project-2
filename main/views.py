from django.shortcuts import render
from apps.product.models import Product

# Create your views here.

def index(request):
    featured_products = Product.objects.all()[:3]
    context = {
        "featured_products": featured_products
    }
    return render(request, 'index.html', context)

def about(request):
    return render(request, 'main/about.html')

def contact(request):
    return render(request, 'main/contact.html')
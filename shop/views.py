from django.shortcuts import render
from django.http import HttpResponse
from .models import Product, Contact
from math import ceil

def index(request):
    allprods = []
    catprods = Product.objects.values('category', 'id')
    categories = {item['category'] for item in catprods}
    for cat in categories:
        prod = Product.objects.filter(category = cat)
        n = len(prod)
        nSlides = ceil(n/4)
        allprods.append([prod, range(1, nSlides), nSlides]) 
        
    return render(request, 'shop/index.html', {'allprods' : allprods})

def about(request):
    return render(request, 'shop/about.html')
    
def contact(request):
    if request.method == 'POST':
        ''' Add entry to DB '''
        name = request.POST.get('name', '')
        email = request.POST.get('email', '')
        phone = request.POST.get('phone', '')
        query = request.POST.get('query', '')
        contact = Contact(name=name, email=email, phone=phone, query=query)
        contact.save()
    return render(request, 'shop/contact.html')

def tracker(request):
    return render(request, 'shop/tracker.html')

def search(request):
    return render(request, 'shop/search.html')

def productView(request, iden):
    prod = Product.objects.filter(id = iden)
    return render(request, 'shop/prodview.html', {'product' : prod[0]})

def checkout(request):
    return render(request, 'shop/checkout.html')
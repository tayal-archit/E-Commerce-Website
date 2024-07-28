from django.shortcuts import render
from django.http import HttpResponse
from .models import Product, Contact, Orders
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

def searchMatch(query, item):
    query = query.lower()
    if query in item.product_name.lower() or query in item.category.lower() or query in item.desc.lower():
        return True
    else:
        return False
    
def search(request):
    query= request.GET.get('search')
    allProds = []
    catprods = Product.objects.values('category', 'id')
    cats = {item['category'] for item in catprods}
    for cat in cats:
        prodtemp = Product.objects.filter(category=cat)
        prod=[item for item in prodtemp if searchMatch(query, item)]
        n = len(prod)
        nSlides = ceil(n / 4)
        if len(prod)!= 0:
            allProds.append([prod, range(1, nSlides), nSlides])
    params = {'allprods': allProds, "msg":""}
    if len(allProds)==0:
        params={'msg':"Please make sure to enter relevant search query"}
    return render(request, 'shop/search.html', params)

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
        thank=True
        return render(request, 'shop/contact.html', {'thank':thank})
        
    return render(request, 'shop/contact.html')

def tracker(request):
    return render(request, 'shop/tracker.html')

def productView(request, iden):
    prod = Product.objects.filter(id = iden)
    return render(request, 'shop/prodview.html', {'product' : prod[0]})

def checkout(request):
    if request.method=="POST":
        items_json= request.POST.get('itemsJson', '')
        amount = request.POST.get('amount', '')
        name=request.POST.get('name', '')
        email=request.POST.get('email', '')
        address=request.POST.get('address1', '') + " " + request.POST.get('address2', '')
        city=request.POST.get('city', '')
        state=request.POST.get('state', '')
        zip_code=request.POST.get('zip_code', '')
        phone=request.POST.get('phone', '')

        order = Orders(items_json= items_json, name=name, email=email, address= address, city=city, state=state, zip_code=zip_code, phone=phone, amount=amount)
        order.save()
        thank=True
        id=order.order_id
        return render(request, 'shop/checkout.html', {'thank':thank, 'id':id})
    return render(request, 'shop/checkout.html')
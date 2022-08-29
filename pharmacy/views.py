from django.shortcuts import render, redirect
from .models import *
from datetime import date
from accounts.models import *
import accounts.views as account_views
from .forms import ProductForm
from product.models import Product
from order.models import *
from item.models import *

# Create your views here.


def signup(request):
    if request.method == "POST":
        print(request.POST)
        manager_name = request.POST['manager_name']
        shop_name = request.POST['shop_name']
        email = request.POST['email']
        mobile_no = request.POST['phone']
        address = request.POST['address']
        password = request.POST['password']


        #push this data in the database
        pharmacy = Pharmacy(manager_name=manager_name, shop_name=shop_name, email=email, mobile_no=mobile_no, address=address, password=password)
        pharmacy.save()

        acc = Account(email=email, password=password, usertype='Pharmacy')
        acc.save()

        #redirect to login
        return render(request, "Accounts/home.html", {})

    return render(request, "pharmacy/Signup.html", {})


def load_pharmacy(request, name):
    # print("this is a function")

    pharmacy_id = request.session['pharmacy']

    pharmacy = Pharmacy.objects.get(id=pharmacy_id)

    context = {
        'pharmacy_id': pharmacy.id,
        'name': pharmacy.shop_name
    }

    return render(request, 'pharmacy/home.html', context)


def show_products(request):
    pharmacy_id = request.session['pharmacy']
    pharmacy = Pharmacy.objects.get(id=pharmacy_id)
    products = Product.objects.filter(shop_id=pharmacy_id)
    context = {
        'pharmacy_id': pharmacy.id,
        'name': pharmacy.shop_name,
        'products': products
    }
    return render(request, 'pharmacy/show_products.html', context)


def add_product(request):
    pharmacy_id = request.session['pharmacy']
    pharmacy = Pharmacy.objects.get(id=pharmacy_id)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False) # Because we have not given vendor yet
            product.shop_id = pharmacy_id
            # product.slug = slugify(product.title)
            product.save() #finally save
            products = Product.objects.filter(shop_id=pharmacy_id)
            context = {
                'pharmacy_id': pharmacy.id,
                'name': pharmacy.shop_name,
                'products': products
            }

        return render(request, 'pharmacy/show_products.html', context)


    else:
        form = ProductForm
    
    context = {
        'pharmacy_id': pharmacy.id,
        'name': pharmacy.shop_name,
        'form': form
    }

    return render(request, 'pharmacy/add_product.html', context)

def show_orders(request):
    pharmacy_id = request.session['pharmacy']
    pharmacy = Pharmacy.objects.get(id=pharmacy_id)
    orders = Order.objects.filter(pharmacy_id=pharmacy_id)
    context = {
        'pharmacy_id': pharmacy.id,
        'name': pharmacy.shop_name,
        'orders': orders
    }

    if request.method == "POST":
        order_id = request.POST.get('selected')
        status = request.POST.get('status')
        if status == None:
            order = Order.objects.get(id=order_id)
            items = Item.objects.filter(order_id=request.POST.get('selected'))
            total = 0
            for item in items:
                total += item.total
            c = {
                'order': order,
                'order_id': order_id,
                'items': items,
                'total': total
            }
            return render(request, 'pharmacy/show_details.html', c)
        
        else:
            order = Order.objects.get(id=status)
            st = order.status
            if st == 'Pending':
                order.status = 'Accepted'
                order.save()
            return render(request, 'pharmacy/show_orders.html', context)
        

    return render(request, 'pharmacy/show_orders.html', context)


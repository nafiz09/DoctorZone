from django.shortcuts import render, redirect
from .models import *
from datetime import date
from accounts.models import *
import accounts.views as account_views
from product.models import *
from pharmacy.models import *
# Create your views here.

def signup(request):
    if request.method == "POST":
        print(request.POST)
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        birthday = request.POST['birthday']
        gender = request.POST['gender']
        if gender == 'on':
            gender = 'M'
        else:
            gender = 'F'
        email = request.POST['email']
        mobile_no = request.POST['phone']
        address = request.POST['address']
        password = request.POST['password']

        birthday = birthday.split("/")
        birthday = date(int(birthday[2]), int(birthday[1]), int(birthday[0]))

        #push this data in the database
        patient = Patient(first_name=first_name, last_name=last_name, birthday=birthday, gender=gender, email=email
                          , mobile_no=mobile_no, address=address, password=password)
        patient.save()

        acc = Account(email=email, password=password, usertype='Patient')
        acc.save()

        #redirect to login
        return render(request, "Accounts/home.html", {})

    return render(request, "Patient/Signup/registration.html", {})


def load_patient(request, name):
    print("this is a function")

    patient_id = request.session['patient']

    patient = Patient.objects.get(id=patient_id)

    context = {
        'patient_id': patient.id,
        'name': patient.first_name + " " + patient.last_name
    }

    return render(request, 'Patient/Home/home.html', context)


def show_products(request):
    products = Product.objects.all()
    pharmacy = {}
    # for p in products:
    #     shop = Pharmacy.objects.get(id=p.shop_id)
    #     pharmacy[p.id] = shop.shop_name
    
    # print(pharmacy.get(13))


    context = {
        'products': products,
        'pharmacy': pharmacy
    }

    return render(request, 'Patient/products.html', context)

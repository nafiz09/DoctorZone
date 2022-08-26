from django.shortcuts import render
from deliveryman.models import *
from accounts.models import *
from datetime import date, timedelta
from order.models import *

# Create your views here.


def signup(request):
        if request.method == "POST":
            print(request.POST)
            first_name = request.POST['first_name']
            last_name = request.POST['last_name']
            birthday = request.POST['birthday']
            email = request.POST['email']
            mobile_no = request.POST['phone']
            address = request.POST['address']
            password = request.POST['password']

            birthday = birthday.split("/")
            birthday = date(int(birthday[2]), int(birthday[1]), int(birthday[0]))

            #push this data in the database
            deliveryman = Deliveryman(first_name=first_name, last_name=last_name, birthday=birthday, email=email
                            , mobile_no=mobile_no, address=address, password=password)
            deliveryman.save()

            acc = Account(email=email, password=password, usertype='Deliveryman')
            acc.save()

            #redirect to login
            return render(request, "Accounts/home.html", {})

        return render(request, "Deliveryman/registration.html", {})


def load_deliveryman(request, name):
    # print("this is a function")

    deliveryman_id = request.session['deliveryman']

    deliveryman = Deliveryman.objects.get(id=deliveryman_id)
    name = deliveryman.first_name + " " + deliveryman.last_name

    context = {
        'deliveryman_id': deliveryman.id,
        'name': name
    }

    return render(request, 'deliveryman/home.html', context)

def pending_orders(request):
    deliveryman_id = request.session['deliveryman']
    deliveryman = Deliveryman.objects.get(id=deliveryman_id)
    orders = Order.objects.filter(status='Accepted')
    context = {
        'deliveryman_id': deliveryman.id,
        'name': deliveryman.first_name,
        'orders': orders
    }
    if request.method == "POST":
        order_id = request.POST.get('selected')
        st = request.POST.get('status')
        if st == None:
            order = Order.objects.get(id=order_id)
            c = {
                'deliveryman_id': deliveryman.id,
                'name': deliveryman.first_name,
                'order': order
                }
            return render(request, 'deliveryman/show_details.html', c)
        else:
            order = Order.objects.get(id=st)
            order.status = 'Got_deliveryman'
            order.save()
            return render(request, 'deliveryman/pending_orders.html', context)

    return render(request, 'deliveryman/pending_orders.html', context)

    
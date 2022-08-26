from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.http import HttpResponse
import accounts.models
import doctor.views as doctor_views
import patient.views as patient_views
from doctor.models import *
from patient.models import *
from pharmacy.models import *
from accounts.models import *
from deliveryman.models import *


def login(request):

    # check if the session has doctor_id in dictionary 'doctor'
    # then get the doctor with the id
    # redirect to a specific url, and send a parameter in the url as well
    # that name will be in the url pattern

    if 'doctor' in request.session:
        doctor = Doctor.objects.get(id=request.session['doctor'])
        return redirect(reverse('doctor:home', kwargs={'name': doctor.first_name}))
    elif 'patient' in request.session:
        patient = Patient.objects.get(id=request.session['patient'])
        return redirect(reverse('patient:home', kwargs={'name': patient.first_name}))
    elif 'pharmacy' in request.session:
        pharmacy = Pharmacy.objects.get(id=request.session['pharmacy'])
        return redirect(reverse('pharmacy:home', kwargs={'name': pharmacy.id}))
    elif 'deliveryman' in request.session:
        deliveryman = Deliveryman.objects.get(id=request.session['deliveryman'])
        return redirect(reverse('deliveryman:home', kwargs={'name': deliveryman.id}))

    # if no session alive, show login page
    else:
        if request.method == "POST":
            print(request.POST)
            email = request.POST['email']
            password = request.POST['password']

            # try to match the password with "Accounts" table
            try:
                account = Account.objects.get(email=email)
                print(account)
                accpass = account.password
                if password == accpass:
            # if matched, see user type and redirect to their own home page
                    if account.usertype == "Doctor":
                        doctor = Doctor.objects.get(email=email)
            # insert the person's doctor_id in the session as dictionary 'doctor'
                        request.session['doctor'] = doctor.id
                        print(2)
            # parameter name is passed to the url.py to append to the url
                        return redirect(reverse('doctor:home', kwargs={'name': doctor.first_name}))
                    elif account.usertype == "Patient":
                        patient = Patient.objects.get(email=email)
                        request.session['patient'] = patient.id
                        # print('p')
                        return redirect(reverse('patient:home', kwargs={'name': patient.first_name}))
                    elif account.usertype == "Pharmacy":
                        pharmacy = Pharmacy.objects.get(email=email)
                        request.session['pharmacy'] = pharmacy.id
                        print('p')
                        return redirect(reverse('pharmacy:home', kwargs={'name': pharmacy.id}))
                    elif account.usertype == "Deliveryman":
                        deliveryman = Deliveryman.objects.get(email=email)
                        request.session['deliveryman'] = deliveryman.id
                        print('pain')
                        return redirect(reverse('deliveryman:home', kwargs={'name': deliveryman.id}))

            # if user doesn't exist after querying, error comes, show the home page
            except:
                print("except")
                return render(request, "Accounts/home.html", {})

    # if no password matched, redirect to home page ...
    # Accounts/home_old.html = login page
    return render(request, "Accounts/home.html", {})

# check for the password and login


def delete_session(request):
    request.session.flush()
    request.session.clear_expired()
    return redirect(reverse('main_home'))

def landing_home(request):
    return render(request, 'home.html')

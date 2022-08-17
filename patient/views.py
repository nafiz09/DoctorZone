import datetime

from django.http import JsonResponse
from django.urls import reverse
from django.shortcuts import render, redirect
from .models import *
from datetime import date, timedelta
from django.utils import timezone
from accounts.models import *
from doctor.models import *
import doctor.views as doctor_views
import accounts.views as account_views
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
    if 'patient' not in request.session:
        return redirect(reverse('main_home'))
    print("qwertyui")
    print("this is a function")

    patient_id = request.session['patient']

    patient = Patient.objects.get(id=patient_id)

    context = {
        'patient': patient,
        'patient_id': patient.id,
        'name': patient.first_name + " " + patient.last_name
    }

    return render(request, 'Patient/Home/home.html', context)


def search_result(request, name):
    if 'patient' not in request.session:
        return redirect(reverse('main_home'))

    doctors = Doctor.objects.all()
    # after searching I have some id's of DOCTOR that match the search
    print("doctors")
    print(doctors)
    chambersList = []
    for doctor in doctors:
        chamber_info_list = doctor_views.setupChamberList(doctor.id)
        if len(chamber_info_list) == 0:
            continue
        print("chamber- info list")
        print(chamber_info_list)
        chambersList.append(chamber_info_list)
        chambersList = chambersList[0]
        print("chamberlist")
        print(chambersList)

    print(chambersList)
    context = {
        'chambers': chambersList,
        'patient': Patient.objects.get(id=request.session['patient'])
    }
    print("take appointment --")
    print(context)
    return render(request, "Patient/Home/search_result.html", context)


def take_appointment(request, name, chamber_id):
    if 'patient' not in request.session:
        return redirect(reverse('main_home'))

    patient = Patient.objects.get(id=request.session['patient'])
    chamber = Chamber.objects.get(id=chamber_id)
    if request.method == 'POST':
        print(request.POST)
        msg = request.POST['Date_Radio']
        # '2022-08-15  ---------  Serial no : 1
        msg = msg.split(' ')
        msg = msg[0]
        app_date = datetime.datetime.strptime(msg, '%Y-%m-%d').date()
        print(app_date)
        appointment = Appointment(patient=patient, chamber=chamber, date=app_date)
        appointment.save()
        return redirect(reverse('patient:home', kwargs={'name': patient.first_name}))

    chamber = Chamber.objects.get(id=chamber_id)
    appointment_dates = produce_valid_dates(chamber) #str valid dates
    appointment_details = []
    # time can be calculated
    for date in appointment_dates:
        serial = len(Appointment.objects.filter(date=date, chamber_id=chamber_id))
        appointment_details.append(date + "  ---------  Serial no : " + str(serial+1))

    context = {
        'appointment_dates': appointment_details,
        'patient': patient,
        'chamber_id': chamber_id
    }
    return render(request, "Patient/Appointment/appointment.html", context)


def produce_valid_dates(chamber):
    # if saturday open = 5, if sunday open = 6................if friday open =

    day_list = []
    if str(chamber.mon_starttime) != "00:00:00" and str(chamber.mon_endtime) != "00:00:00":
        day_list.append(1)
    else:
        day_list.append(0)
    if str(chamber.tues_starttime) != "00:00:00" and str(chamber.tues_endtime) != "00:00:00":
        day_list.append(1)
    else:
        day_list.append(0)
    if str(chamber.wed_starttime) != "00:00:00" and str(chamber.wed_endtime) != "00:00:00":
        day_list.append(1)
    else:
        day_list.append(0)
    if str(chamber.thrs_starttime) != "00:00:00" and str(chamber.thrs_endtime) != "00:00:00":
        day_list.append(1)
    else:
        day_list.append(0)
    if str(chamber.fri_starttime) != "00:00:00" and str(chamber.fri_endtime) != "00:00:00":
        day_list.append(1)
    else:
        day_list.append(0)
    if str(chamber.sat_starttime) != "00:00:00" and str(chamber.sat_endtime) != "00:00:00":
        day_list.append(1)
    else:
        day_list.append(0)
    if str(chamber.sun_starttime) != "00:00:00" and str(chamber.sun_endtime) != "00:00:00":
        day_list.append(1)
    else:
        day_list.append(0)

    print(day_list)
    date = datetime.date.today()
    # 2022-08-13       # datetime.date
    print("today's date in datetime.date : " + str(date) + " and type : " + str(type(date)))
    today_date = str(date)
    # weekday Monday = 0 , Sunday = 6
    print("today weekday : " + str(date.weekday()) + " and type : " + str(type(date)))

    # same code
    # date = datetime.date.today() // datetime.datetime.now().date()
    # print(date)  # 2022-08-13
    # print(type(date))  # datetime.date
    # today_date = str(date)  # 2022-08-13
    # print(today_date)

    # type resolving done
    # timedelta(days=)
    days_tmp=[]
    i = 0
    for day in day_list:
        if day == 1:
            days_tmp.append(i)
        i = i + 1
    # mon fri sat
    # 0    4   6 (starting from monday = 0)
    # -3    1   2     (-4)  suppose today friday = 4
    # 4     1   2   if negative (+7)
    print(days_tmp)
    days = []
    for day in days_tmp:
        day = day - int(date.weekday())
        if day < 0:
            day += 7
        days.append(day)
    # days = [4,1,2]
    # this means 4 or 1 or 2 can be added to current date to get a valid date
    # if today friday , +4 means tuesday date, +1 means saturday date, +2 means sunday date
    days.sort()
    print("days " + str(days))

    valid_date_list = []
    while True:
        for i in range(0, len(days)):
            date_candidate = date + timedelta(days=days[i])
            if check_valid_date(date_candidate, chamber.id):
                valid_date_list.append(str(date_candidate))
            days[i] += 7
            if len(valid_date_list) == len(days):
                break
        break
    return valid_date_list

# for each valid date,check capacity
# need to work here


def check_valid_date(date, chamber_id):
    return True

# def show_profile_public(request, patient_id):


def show_appointments(request, name):
    if 'patient' not in request.session:
        return redirect(reverse('main_home'))

    patient = Patient.objects.get(id=request.session['patient'])

    print('haha')
    appointments = Appointment.objects.filter(patient_id=patient.id).order_by('-date')
    print('appointments')
    print(len(appointments))

    appmntList = []
    for app in appointments:
        dic = {}
        print("inside")
        print(app.date)
        dic['date'] = str(app.date)
        dic['chamber_id'] = str(app.chamber_id)
        print(app.chamber_id)
        doctor_name ='Dr. ' + str(Chamber.objects.get(id=app.chamber_id).doctor.first_name)
        dic['doctor_first_name'] = doctor_name
        dic['state'] = app.state
        dic['location'] = str(Chamber.objects.get(id=app.chamber_id).address)
        appmntList.append(dic)

    context = {
        'appointments': appmntList,
        'patient': patient
    }

    return render(request, 'Patient/Appointment/show_appointments.html', context)


def edit_profile(request, name):
    if 'patient' not in request.session:
        return redirect(reverse('main_home'))

    patient = Patient.objects.get(id=request.session['patient'])
    context = { }
    context['patient'] = patient

    return render(request, 'Patient/Home/edit_profile.html', context)


def show_profile(request, name):
    if 'patient' not in request.session:
        return redirect(reverse('main_home'))

    patient = Patient.objects.get(id=request.session['patient'])
    context = { }
    context['patient'] = patient

    return render(request, 'Patient/Home/show_profile.html', context)


def ageCalculator(date):
    return True


def show_products(request, name):
    if 'patient' not in request.session:
        return redirect(reverse('main_home'))
    patient = Patient.objects.get(id=request.session['patient'])
    print("hahastart")
    products = Product.objects.all()
    # for p in products:
    #     shop = Pharmacy.objects.get(id=p.shop_id)
    #     pharmacy[p.id] = shop.shop_name
    
    # print(pharmacy.get(13))


    context = {
        'products': products,
        'patient': patient
    }
    print("haha")
    print(context)
    print("haha1")
    return render(request, 'Patient/products.html', context)

def test_function(request):
    print("inside test function")
    return JsonResponse({})
from django.shortcuts import render, redirect, reverse
from doctor.models import *
from accounts.models import *
from datetime import date, datetime
from django.core import serializers
import accounts.views as account_views


# Create your views here.

def signup(request):
    specialists = [
        "Gynochologist",
        "Eye_Specialist",
        "Cardiologist",
        "Psychiatrist",
        "Psychologist",
        "Gastoentrologist"
    ]

    data = {
        "specialists": specialists
    }

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

        license_no = request.POST['license']
        specialist = request.POST['specialist']
        # MBBS, DMC, 10/12/2000
        degreesAndinstitutesAnddates = request.POST['degrees'].split('\r\n')

        birthday = birthday.split("/")
        birthday = date(int(birthday[2]), int(birthday[1]), int(birthday[0]))

        doctor = Doctor(first_name=first_name, last_name=last_name, birthday=birthday, gender=gender, email=email,
                        mobile_no=mobile_no,
                        address=address, password=password, license_no=license_no, specialist=specialist,
                        verified="pending")

        doctor.save()

        accounts = Account(email=email, password=password, usertype='Doctor')
        accounts.save()

        for data in degreesAndinstitutesAnddates:
            rowdata = data.split(',')
            print(rowdata)
            try:
                print(rowdata[0])
            except IndexError:
                print("Degree name was not given properly.")
            try:
                print(rowdata[1])
            except IndexError:
                print("Degree institute was not given properly.")
            degreeofdoctor = DegreeOfDoctor(doctor=doctor, degree_name=rowdata[0],
                                            institute=rowdata[1])  # , degree_date= )
            try:
                print(rowdata[2])
                degreedate = rowdata[2].split("/")
                degreedate_entry = date(int(degreedate[2]), int(degreedate[1]), int(degreedate[0]))
                degreeofdoctor.degree_date = degreedate_entry
            except IndexError:
                print("Index Should be smaller. Degree date was not given properly.")
            degreeofdoctor.save()

        # redirect to login
        return render(request, "Accounts/home.html", {})

    # return render(request, "Doctor/Signup/Signup.html", data)
    return render(request, "Doctor/Signup/registration.html", data)


def load_doctor_rev(request, name):
    print(f"name -- {name}")
    doctor_id = request.session['doctor']
    doctor = Doctor.objects.get(id=doctor_id)
    # doctor = Doctor.objects.get(email='d@d')
    # doctor = serializers.serialize('json', doctor)
    print(doctor)
    print(doctor.first_name)
    context = {
        'doctor': doctor,
    }

    return render(request, 'Doctor/Home/Home.html', context)


def add_chamber(request, name):
    # if not in session, go to main home
    if 'doctor' not in request.session:
        return redirect(reverse('main_home'))

    print(f"entered adding chamber of -- {name}")
    doctorid = request.session['doctor']
    doctor = Doctor.objects.get(id=doctorid)
    doctor_chambers = Chamber.objects.filter(doctor_id=doctorid)
    print(doctor_chambers)

    context = {
        'doctor': doctor
    }

    #"C"  # "No CHAMBER on this day"
    #"S"  # "START time not defined\n"
    #"E"  # "END time not defined\n"
    #"N"  #NOT VALID #START TIME > END TIME
    #V valid

    if request.method == "POST":
        # after insertion of data, redirect to doctor's home page
        print(request.POST)
        time_list = [request.POST['sat_start_time'], request.POST['sat_end_time'],
                request.POST['sun_start_time'], request.POST['sun_end_time'],
                request.POST['mon_start_time'], request.POST['mon_end_time'],
                request.POST['tues_end_time'], request.POST['tues_end_time'],
                request.POST['wed_start_time'], request.POST['wed_end_time'],
                request.POST['thrs_start_time'], request.POST['thrs_end_time'],
                request.POST['fri_start_time'], request.POST['fri_end_time']
        ]
        weekday_list = ['Saturday', 'Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']
        check = ''
        idle_day_count = 0
        error_msg = ''
        for i in range(0, 14, 2):
            checkTime(time_list[i], time_list[i+1])    #[i] = start time and [i+1]= end time
            if check == "C":
                idle_day_count = idle_day_count+1
            elif check == "S":
                error_msg = error_msg + weekday_list[int(i/2)] + ' START time not defined\n'
            elif check == "E":
                error_msg = error_msg + weekday_list[int(i/2)] + ' END time not defined\n'
            elif check == "N":
                error_msg = error_msg + weekday_list[int(i/2)] + ' START time is AHEAD of END time\n'

        address = request.POST['address']
        payment = int(request.POST['payment'])

        if idle_day_count == 7:
            error_msg = error_msg + "NO days selected for chamber openings \n"


        # chamber = Chamber( sat_starttime=sat_start, sat_endtime=sat_end,
        #                   sun_starttime=sun_start, sun_endtime=sun_end,
        #                   mon_starttime=mon_start, mon_endtime=mon_end,
        #                   tues_starttime=tues_start, tues_endtime=tues_end,
        #                   wed_starttime=wed_start, wed_endtime=wed_end,
        #                   thrs_starttime=sat_start, thrs_endtime=sat_end,
        #                   fri_starttime=fri_start, fri_endtime=fri_end,
        #                   address=address, payment=payment
        #                   )
        # chamber.save()
        return redirect(reverse('doctor:home', kwargs={'name': doctor.first_name}))




    return render(request, 'Doctor/Chambers/add_chamber.html', context)


# #   text is in format '14:50'
# def convert_time(my_time):
#     TIME = datetime.strptime(my_time, "%H:%M")
#     print(TIME)
#     return TIME


def checkTime(start, end):
    if start == '' and end == '':
        return "C"   #"No CHAMBER on this day"
    elif start == '' and end != '':
        return "S"   #"START time not defined"
    elif start != '' and end == '':
        return "E"     #"END time not defined"
    else:
        start = start.split(':')
        end = end.split(':')
        startInMinutes = int(start[0])*60 + int(start[1])
        endInMinutes = int(end[0])*60 + int(end[1])

        #   doctor is sitting for AT LEAST >0 minutes today
        if endInMinutes - startInMinutes > 0:
            return "V"  #VALID
        else:
            return "N"  #NOT VALID #START TIME > END TIME


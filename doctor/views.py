from django.http import HttpResponse
from django.shortcuts import render, redirect, reverse
from django.template.defaultfilters import lower, upper

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

    if 'doctor' not in request.session:
        return redirect(reverse('main_home'))

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

    # "C"  # "No CHAMBER on this day"
    # "S"  # "START time not defined\n"
    # "E"  # "END time not defined\n"
    # "N"  #NOT VALID #START TIME > END TIME
    # V valid


    if request.method == "POST":
        # after insertion of data, redirect to doctor's home page
        print(request.POST)
        time_list = [request.POST['sat_start_time'], request.POST['sat_end_time'],
                     request.POST['sun_start_time'], request.POST['sun_end_time'],
                     request.POST['mon_start_time'], request.POST['mon_end_time'],
                     request.POST['tues_start_time'], request.POST['tues_end_time'],
                     request.POST['wed_start_time'], request.POST['wed_end_time'],
                     request.POST['thrs_start_time'], request.POST['thrs_end_time'],
                     request.POST['fri_start_time'], request.POST['fri_end_time']
                     ]
        weekday_list = ['Saturday', 'Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']
        check = ''
        idle_day_count = 0
        error_msg = []
        for i in range(0, 14, 2):
            check = checkTime(time_list[i], time_list[i + 1])  # [i] = start time and [i+1]= end time
            if check == "C":
                idle_day_count = idle_day_count + 1
                time_list[i] = '00:00'  # default start value if no chamber day = 00:00 (12:00AM)
                time_list[i + 1] = '00:00'  # default value end if no chamber day = 00:00 (12:00AM)
            elif check == "S":
                error_msg.append(weekday_list[int(i / 2)] + ' START time not defined\n')
            elif check == "E":
                error_msg.append(weekday_list[int(i / 2)] + ' END time not defined\n')
            elif check == "N":
                error_msg.append(weekday_list[int(i / 2)] + ' START time is AHEAD of END time\n')

        address = request.POST['address']
        payment = int(request.POST['payment'])

        if idle_day_count == 7:
            error_msg.append("NO days selected for chamber openings \n")
        print(error_msg)
        context_POST = {
            'error_message': error_msg,
            'doctor': doctor
        }

        if len(error_msg) > 0:
            return render(request, "Doctor/Chambers/add_chamber.html", context_POST)
        else:
            # if time_list[0] != "00:00" and time_list[1] != "00:00":
            #     chamber.sat_starttime = time_list[0]
            #     chamber.sat_endtime = time_list[1]
            # if time_list[2] != "00:00" and time_list[3] != "00:00":
            #     chamber.sun_starttime = time_list[2]
            #     chamber.sun_endtime = time_list[3]
            # if time_list[4] != "00:00" and time_list[5] != "00:00":
            #     chamber.mon_starttime = time_list[4]
            #     chamber.mon_endtime = time_list[5]
            # if time_list[6] != "00:00" and time_list[7] != "00:00":
            #     chamber.tues_starttime = time_list[6]
            #     chamber.tues_endtime = time_list[7]
            # if time_list[8] != "00:00" and time_list[9] != "00:00":
            #     chamber.wed_starttime = time_list[8]
            #     chamber.wed_endtime = time_list[9]
            # if time_list[10] != "00:00" and time_list[11] != "00:00":
            #     chamber.thrs_starttime = time_list[10]
            #     chamber.thrs_endtime = time_list[11]
            # if time_list[12] != "00:00" and time_list[13] != "00:00":
            #     chamber.fri_starttime = time_list[12]
            #     chamber.fri_endtime = time_list[13]

            #if edit chamber happens, we will not get address

            # this is add chamber block, create new chamber
            chamber = Chamber(doctor=doctor)

            # This is edit chamber block, get a previous chamber
            chamber.sat_starttime = time_list[0]
            chamber.sat_endtime = time_list[1]
            chamber.sun_starttime = time_list[2]
            chamber.sun_endtime = time_list[3]
            chamber.mon_starttime = time_list[4]
            chamber.mon_endtime = time_list[5]
            chamber.tues_starttime = time_list[6]
            chamber.tues_endtime = time_list[7]
            chamber.wed_starttime = time_list[8]
            chamber.wed_endtime = time_list[9]
            chamber.thrs_starttime = time_list[10]
            chamber.thrs_endtime = time_list[11]
            chamber.fri_starttime = time_list[12]
            chamber.fri_endtime = time_list[13]
            chamber.address = address
            chamber.payment = payment
            chamber.save()

        return redirect(reverse('doctor:home', kwargs={'name': doctor.first_name}))

    return render(request, 'Doctor/Chambers/add_chamber.html', context)


def checkTime(start, end):
    if start == '' and end == '':
        return "C"  # "No CHAMBER on this day"
    elif start == '' and end != '':
        return "S"  # "START time not defined"
    elif start != '' and end == '':
        return "E"  # "END time not defined"
    else:
        start = start.split(':')
        end = end.split(':')
        startInMinutes = int(start[0]) * 60 + int(start[1])
        endInMinutes = int(end[0]) * 60 + int(end[1])

        #   doctor is sitting for AT LEAST >0 minutes today
        if (endInMinutes - startInMinutes > 0) or (endInMinutes == 0 and startInMinutes == 0):
            return "V"  # VALID
        else:
            return "N"  # NOT VALID #START TIME > END TIME


# name variable is sent from the url, to capture to the handler in views.py
def show_chamber(request, name):
    if 'doctor' not in request.session:
        return redirect(reverse('main_home'))
    doctorid = request.session['doctor']
    doctor = Doctor.objects.get(id=doctorid)
    print('inside SHOW CHAMBER of doctor ' + doctor.first_name)
    # print(setupChamberList(doctorid))
    context = {
        'doctor': doctor,
        'chambers': setupChamberList(doctorid)
    }
    return render(request, 'Doctor/Chambers/card_chamber.html', context)


def setupChamberList(doctor_id):
    doctor = Doctor.objects.get(id=doctor_id)
    print(doctor.first_name)
    chambers = Chamber.objects.filter(doctor=doctor)
    chambers_dic_list = []
    print("inside chamber list")
    for chamber in chambers:
        dictionary = {}
        print(chamber.sat_starttime)
        print(chamber.sun_starttime)
        print(type(chamber.sun_starttime))
        print(str(chamber.sun_starttime))
        print(type(str(chamber.sun_starttime)))
        if str(chamber.sat_starttime) != "00:00:00" and str(chamber.sat_endtime) != "00:00:00":
            dictionary["sat"] = "Saturday--Start-time : " + str(chamber.sat_starttime) + " End-time : " + str(
                chamber.sat_endtime)
        if str(chamber.sun_starttime) != "00:00:00" and str(chamber.sun_endtime) != "00:00:00":
            dictionary["sun"] = "Sunday--Start-time : " + str(chamber.sun_starttime) + " End-time : " + str(
                chamber.sun_endtime)
        if str(chamber.mon_starttime) != "00:00:00" and str(chamber.mon_endtime) != "00:00:00":
            dictionary["mon"] = "Monday--Start-time : " + str(chamber.mon_starttime) + " End-time : " + str(
                chamber.mon_endtime)
        if str(chamber.tues_starttime) != "00:00:00" and str(chamber.tues_endtime) != "00:00:00":
            dictionary["tues"] = "Tuesday--Start-time : " + str(chamber.tues_starttime) + " End-time : " + str(
                chamber.tues_endtime)
        if str(chamber.wed_starttime) != "00:00:00" and str(chamber.wed_endtime) != "00:00:00":
            dictionary["wed"] = "Wednesday--Start-time : " + str(chamber.wed_starttime) + " End-time : " + str(
                chamber.wed_endtime)
        if str(chamber.thrs_starttime) != "00:00:00" and str(chamber.thrs_endtime) != "00:00:00":
            dictionary["thrs"] = "Thursday--Start-time : " + str(chamber.thrs_starttime) + " End-time : " + str(
                chamber.thrs_endtime)
        if str(chamber.fri_starttime) != "00:00:00" and str(chamber.fri_endtime) != "00:00:00":
            dictionary["fri"] = "Friday--Start-time : " + str(chamber.fri_starttime) + " End-time : " + str(
                chamber.fri_endtime)
        dictionary['payment'] = str(chamber.payment)
        dictionary['chamber_id'] = str(chamber.id)
        dictionary['doctor_name'] = str("Dr. " + doctor.first_name + " " + doctor.last_name)
        print("each chamber info")
        print(dictionary)
        chambers_dic_list.append(dictionary)
        # dictionary = {
        #     "sat_starttime" : chamber.sat_starttime, "sat_endtime" : chamber.sat_endtime,
        #     "sun_starttime": chamber.sun_starttime, "sun_endtime": chamber.sun_endtime,
        #     "mon_starttime": chamber.mon_starttime, "mon_endtime": chamber.mon_endtime,
        #     "tues_starttime": chamber.tues_starttime, "tues_endtime": chamber.tues_endtime,
        #     "wed_starttime": chamber.wed_starttime, "wed_endtime": chamber.wed_endtime,
        #     "thrs_starttime": chamber.thrs_starttime, "thrs_endtime": chamber.thrs_endtime,
        #     "fri_starttime": chamber.fri_starttime, "fri_endtime": chamber.fri_endtime,
        #     "payment": chamber.payment, "address": chamber.address
        # }

    print(chambers_dic_list)
    return chambers_dic_list


def edit_chamber(request, name, chamber_id):
    if 'doctor' not in request.session :
        return redirect(reverse('main_home'))

    print(f"entered editing chamber of -- {name}")
    doctorid = request.session['doctor']
    doctor = Doctor.objects.get(id=doctorid)
    context = {
        'doctor': doctor
    }

    # "C"  # "No CHAMBER on this day"
    # "S"  # "START time not defined\n"
    # "E"  # "END time not defined\n"
    # "N"  #NOT VALID #START TIME > END TIME
    # V valid

    chamber = Chamber.objects.get(id=chamber_id)
    #   creating context to show default values of fields
    context = {
        'payment': str(chamber.payment),
        'address': str(chamber.address),
        'doctor': doctor,
        'chamber_id': chamber_id
    }
    if str(chamber.sat_starttime) != "00:00:00" and str(chamber.sat_endtime) != "00:00:00":
        context['sat_starttime'] = str(chamber.sat_starttime)
        context['sat_endtime'] = str(chamber.sat_endtime)
    if str(chamber.sun_starttime) != "00:00:00" and str(chamber.sun_endtime) != "00:00:00":
        context['sun_starttime'] = str(chamber.sun_starttime)
        context['sun_endtime'] = str(chamber.sun_endtime)
    if str(chamber.mon_starttime) != "00:00:00" and str(chamber.mon_endtime) != "00:00:00":
        context['mon_starttime'] = str(chamber.mon_starttime)
        context['mon_endtime'] = str(chamber.mon_endtime)
    if str(chamber.tues_starttime) != "00:00:00" and str(chamber.tues_endtime) != "00:00:00":
        context['tues_starttime'] = str(chamber.tues_starttime)
        context['tues_endtime'] = str(chamber.tues_endtime)
    if str(chamber.wed_starttime) != "00:00:00" and str(chamber.wed_endtime) != "00:00:00":
        context['wed_starttime'] = str(chamber.wed_starttime)
        context['wed_endtime'] = str(chamber.wed_endtime)
    if str(chamber.thrs_starttime) != "00:00:00" and str(chamber.thrs_endtime) != "00:00:00":
        context['thrs_starttime'] = str(chamber.thrs_starttime)
        context['thrs_endtime'] = str(chamber.thrs_endtime)
    if str(chamber.fri_starttime) != "00:00:00" and str(chamber.fri_endtime) != "00:00:00":
        context['fri_starttime'] = str(chamber.fri_starttime)
        context['fri_endtime'] = str(chamber.sat_endtime)


    if request.method == "POST":
        # after insertion of data, redirect to doctor's home page
        print(request.POST)
        time_list = [request.POST['sat_start_time'], request.POST['sat_end_time'],
                     request.POST['sun_start_time'], request.POST['sun_end_time'],
                     request.POST['mon_start_time'], request.POST['mon_end_time'],
                     request.POST['tues_start_time'], request.POST['tues_end_time'],
                     request.POST['wed_start_time'], request.POST['wed_end_time'],
                     request.POST['thrs_start_time'], request.POST['thrs_end_time'],
                     request.POST['fri_start_time'], request.POST['fri_end_time']
                     ]
        weekday_list = ['Saturday', 'Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']
        check = ''
        idle_day_count = 0
        error_msg = []
        for i in range(0, 14, 2):
            check = checkTime(time_list[i], time_list[i + 1])  # [i] = start time and [i+1]= end time
            if check == "C":
                idle_day_count = idle_day_count + 1
                time_list[i] = '00:00'  # default start value if no chamber day = 00:00 (12:00AM)
                time_list[i + 1] = '00:00'  # default value end if no chamber day = 00:00 (12:00AM)
            elif check == "S":
                error_msg.append(weekday_list[int(i / 2)] + ' START time not defined\n')
            elif check == "E":
                error_msg.append(weekday_list[int(i / 2)] + ' END time not defined\n')
            elif check == "N":
                error_msg.append(weekday_list[int(i / 2)] + ' START time is AHEAD of END time\n')

        address = request.POST['address']
        payment = int(request.POST['payment'])

        # if idle_day_count == 7:
        #     error_msg.append("NO days selected for chamber openings \n")
        print(error_msg)
        context_POST = context

        if len(error_msg) > 0:
            context_POST['error_message'] = error_msg
            return render(request, "Doctor/Chambers/edit_chamber.html", context_POST)
        else:
            chamber = Chamber.objects.get(id=chamber_id)
            # This is edit chamber block, get a previous chamber
            chamber.sat_starttime = time_list[0]
            chamber.sat_endtime = time_list[1]
            chamber.sun_starttime = time_list[2]
            chamber.sun_endtime = time_list[3]
            chamber.mon_starttime = time_list[4]
            chamber.mon_endtime = time_list[5]
            chamber.tues_starttime = time_list[6]
            chamber.tues_endtime = time_list[7]
            chamber.wed_starttime = time_list[8]
            chamber.wed_endtime = time_list[9]
            chamber.thrs_starttime = time_list[10]
            chamber.thrs_endtime = time_list[11]
            chamber.fri_starttime = time_list[12]
            chamber.fri_endtime = time_list[13]
            chamber.address = address
            chamber.payment = payment
            chamber.save()

        return redirect(reverse('doctor:show_chamber', kwargs={'name': doctor.first_name}))

    return render(request, 'Doctor/Chambers/edit_chamber.html', context)


def show_appointments_chamber(request, name, chamber_id):
    if 'doctor' not in request.session :
        return redirect(reverse('main_home'))
    doctor = Doctor.objects.get(id=request.session['doctor'])
    chamber = Chamber.objects.get(id=chamber_id)
    appointment_data = Appointment.objects.filter(state='Requested', chamber=chamber, date__gte=date.today())
    print('appointment data')
    print(appointment_data)
    distinct_date = Appointment.objects.filter(chamber=chamber, date__gte=date.today(), state='Requested').values('date').distinct()
    dates = []
    date_appmntList_dict = {}
    for data in distinct_date:
        dates.append(str(data['date']))
        description = "some problem. demo problem statement"
        appmntList = []
        dict = {}
        for in_data in appointment_data:
            print("checking print1 " + str(in_data.date))
            print("checking print2 " + str(data['date']))
            if str(in_data.date) == str(data['date']):
                patient = Patient.objects.get(id=in_data.patient.id)
                print("name : "+in_data.patient.first_name + " " + in_data.patient.last_name)
                dict = {
                    'patient': in_data.patient.first_name + " " + in_data.patient.last_name,
                    'description': description,
                    'patient_id': patient.id,
                    'appointment_id': in_data.id
                }
                appmntList.append(dict)
                dict = {}
        date_appmntList_dict[str(data['date'])] = appmntList
    # print(distinct_date)
    print(date_appmntList_dict)
    print(dates)
    appointments = []
    for data in appointment_data:
        patient = Patient.objects.get(id=data.patient.id)
        dict = {
            'patient': patient.first_name + " " + patient.last_name,
            'patient_id': patient.id,
            'date': str(data.date)
            # 'dates': dates   # dates in which there are appointment
        }
        print("haha")
        appointments.append(dict)
    print()
    context = {
        'doctor': doctor,
        'chamber': chamber,
        'appointments': date_appmntList_dict,
        'dates': dates                  # distinct date list
    }
    print("printing context")
    print(context)
    return render(request, 'Doctor/Appointment/show_appointments.html', context)


def customize_prescription(request, name):
    if 'doctor' not in request.session:
        return redirect(reverse('main_home'))
    doctor = Doctor.objects.get(id=request.session['doctor'])

    presType = doctor.prescriptionFields
    presFields = presType.split("#")
    print(presFields)
    print(len(presFields))
    context = {
        'prescriptionFields': presFields,
        'doctor': doctor
    }
    if request.method == 'POST':
        print(request.POST)
        # presType.append('#'+request.POST['add_field'])
        presType = doctor.prescriptionFields
        presFields = presType.split("#")
        non_delete_fields = ['NAME', 'AGE', 'SEX', 'PROBLEM DESCRIPTION', 'DIAGNOSIS', 'TEST', 'MEDICINE DOSAGE DESCRIPTION']

        if request.POST['delete_field'] != '':
            delete_field = upper(request.POST['delete_field'])
            if delete_field not in non_delete_fields and delete_field in presFields:
                presFields.remove(delete_field)
        if request.POST['add_field'] != '':
            add_field = upper(request.POST['add_field'])
            if add_field not in non_delete_fields:
                presFields.append(add_field)

        presType = ''
        i = 0
        for field in presFields:
            presType += upper(field)
            print("i " + str(i) + " presfield len : " + str(len(presType)))
            print("presType " + presType)
            if i < len(presFields)-1:
                presType += '#'
            i += 1
        print("last")
        print(presType)
        doctor.prescriptionFields = presType
        doctor.save()
        context = {
            'prescriptionFields': presFields,
            'doctor': Doctor.objects.get(id=request.session['doctor'])
        }
    print("context")
    print(context)
    return render(request, 'Doctor/Home/prescription_customization.html', context)


def show_profile(request, name):
    if 'doctor' not in request.session:
        return redirect(reverse('main_home'))
    doctor = Doctor.objects.get(id=request.session['doctor'])
    degrees = DegreeOfDoctor.objects.filter(doctor_id=doctor.id)

    context = {
        'doctor': doctor,
        'degrees': degrees
    }

    return render(request, 'Doctor/Home/show_profile.html', context)


def show_patient_profile(request, name, patient_id):
    if 'doctor' not in request.session:
        return redirect(reverse('main_home'))
    doctor = Doctor.objects.get(id=request.session['doctor'])

    patient = Patient.objects.get(id=patient_id)

    context = {
        'patient': patient,
        'doctor': doctor,
    }
    return render(request, 'Doctor/Appointment/show_patient_public.html', context)


def age(birthdate):
    today = date.today()
    age = today.year - birthdate.year - ((today.month, today.day) < (birthdate.month, birthdate.day))
    return age


def input_OTP(request, name, appointment_id):
    if 'doctor' not in request.session:
        return redirect(reverse('main_home'))

    doctor = Doctor.objects.get(id=request.session['doctor'])
    appointment = Appointment.objects.get(id=appointment_id)

    patient = Patient.objects.get(id=appointment.patient.id)

    if request.method == 'POST':
        input_otp = request.POST['otp']
        if int(appointment.otp) == int(input_otp):
            print("verification done")
            return redirect(reverse('doctor:write_prescription', kwargs={'name': doctor.first_name, 'appointment_id': appointment_id}))
        else:
            chamber_id = appointment.chamber.id
            return redirect(reverse('doctor:show_appointments_chamber', kwargs={'name': doctor.first_name, 'chamber_id': chamber_id}))
    context = {
        'patient': patient,
        'doctor': doctor,
        'appointment_id': appointment_id
    }

    return render(request, 'Doctor/Appointment/input_OTP.html', context)


def write_prescription(request, name, appointment_id):
    if 'doctor' not in request.session:
        return redirect(reverse('main_home'))

    doctor = Doctor.objects.get(id=request.session['doctor'])
    appointment = Appointment.objects.get(id=appointment_id)
    patient = appointment.patient

#   default='NAME#AGE#SEX#PROBLEM DESCRIPTION#DIAGNOSIS#TEST'

#   medicine dosage diagnosis

    print(doctor.prescriptionFields.split('#'))
    presFields = doctor.prescriptionFields.split('#')

    presValues = {}
    presValues['NAME'] = patient.first_name+' '+patient.last_name
    presValues['SEX'] = patient.gender
    presValues['AGE'] = age(patient.birthday)
    # presValues['PROBLEM DESCRIPTION'] = ''
    # presValues['DIAGNOSIS'] = ''
    # presValues['TEST'] = ''


    context = {
        'patient': patient,
        'doctor': doctor,
        'patient_age': age(patient.birthday),
        'Prescription_Fields': presFields[6:],  #exclude name, sex and age
        'appointment_id': appointment_id
    }

    print('prescription context')
    print(context)

    if request.method == 'POST':
        print(request.POST)
        presValues['PROBLEM DESCRIPTION'] = request.POST['problem_description']
        presValues['DIAGNOSIS'] = request.POST['diagnosis']

        test_list = []
        if request.POST['test'] != '':
            test_list.append(request.POST['test'])
        variable = 'test_'
        i = 1
        var = variable+str(i)
        # print(request.POST.get('test_3', 'hahaha'))
        new_test = request.POST.get(var, '')
        while new_test != '':
            test_list.append(new_test)
            i = i + 1
            var = variable + str(i)
            new_test = request.POST.get(var, '')

        test_string = ''
        for i in range(0, len(test_list)):
            if i != (len(test_list)-1):
                test_string = test_string + test_list[i] + '$'
            else:
                test_string = test_string + test_list[i]
        print('test_string')
        print(test_string)
        presValues['TEST'] = test_string
        #test string done alright

        medicine_list = []
        dose_list = []
        med_des_list = []
        variable_med = 'medicine'
        variable_dose = 'dosage'
        variable_des = 'description'
        i = 1
        var_med = variable_med + str(i)
        var_dose = variable_dose + str(i)
        var_des = variable_des + str(i)
        new_med = request.POST.get(var_med, '')

        while new_med != '':
            medicine_list.append(new_med)
            new_dose = request.POST.get(var_dose, '')
            dose_list.append(new_dose)
            new_des = request.POST.get(var_des, '')
            med_des_list.append(new_des)
            i = i + 1
            var_med = variable_med + str(i)
            var_dose = variable_dose + str(i)
            var_des = variable_des + str(i)
            new_med = request.POST.get(var_med, '')

        medicine_string = ''
        for i in range(0, len(medicine_list)):
            each_med_all = medicine_list[i] + '%' + dose_list[i] + '%' + med_des_list[i]

            if i != (len(medicine_list)-1):
                medicine_string = medicine_string + each_med_all + '$'
            else:
                medicine_string = medicine_string + each_med_all

        print('medicine string')
        print(medicine_string)
        presValues['MEDICINE DOSAGE DESCRIPTION'] = medicine_string
        presFields_extra = presFields[7:]

        for field in presFields_extra:
            presValues[field] = request.POST.get(field, '')

        prescription = ''
        for key, value in presValues.items():
            print(str(key) + '--->' +str(value))
            prescription = prescription + str(key) + '&' + str(value) + '#'

        prescription = prescription[:-1]
        print('full prescription')
        print(prescription)
        appointment.prescription = prescription
        appointment.save()
        #alhamdulillah done
        context = {
            'Prescription': prescriptionToDict(appointment_id),
            'doctor': doctor,
            'patient': patient,
            'appointment_id': appointment_id
        }
        return render(request, 'Doctor/Appointment/show_prescription.html', context)

    return render(request, 'Doctor/Appointment/write_prescription.html', context)


def prescriptionToDict(appointment_id):
    prescription = Appointment.objects.get(id=appointment_id).prescription

    prescription_list = prescription.split('#')
    Dict = {}
    doctor = Appointment.objects.get(id=appointment_id).chamber.doctor
    # value = 'Dr.' + str(doctor.first_name) + ' ' + str(doctor.last_name) + '\n'+str(doctor.specialist)+'\n'
    degrees = DegreeOfDoctor.objects.filter(doctor_id=doctor.id)

    doc_info_list = []
    doc_info_list.append('Dr.' + str(doctor.first_name) + ' ' + str(doctor.last_name))
    doc_info_list.append(str(doctor.specialist))

    for degree in degrees:
        doc_info_list.append(str(degree.degree_name) + ', ' + str(degree.institute) + ', ' + str(degree.degree_date))
        # value = value + str(degree.degree_name) + ', ' + str(degree.institute) + ', ' + str(degree.degree_date) + '\n'

    Dict['DOCTOR'] = doc_info_list
    Dict['DATE'] = str(Appointment.objects.get(id=appointment_id).date)

    for i in range(0, len(prescription_list)):
        key_value = prescription_list[i]
        key_value = key_value.split('&')
        key = key_value[0]
        value = key_value[1]
        if key == 'TEST':
            tests_list = value.split('$')
            Dict[key] = tests_list
            continue
            # for test in tests_list:
            #     value = str(j) + '. ' + value + str(test)+'\n'  #1. RBC\n
        elif key == 'MEDICINE DOSAGE DESCRIPTION':
            meds_list = value.split('$')
            print('meds_list')
            print(meds_list)
            # value = ''
            med_dicts_list = []
            for med in meds_list:
                med_dosage_des = med.split('%')
                print('med_dosage_des')
                print(med_dosage_des)
                print('len(med_dosage_des)')
                print(len(med_dosage_des))
                if med_dosage_des[0] == '':
                    print('No medicine added')
                    continue
                med_dict = {}
                med_dict['medicine'] = med_dosage_des[0]
                med_dict['dosage'] = med_dosage_des[1]
                med_dict['description'] = med_dosage_des[2]
                med_dicts_list.append(med_dict)
                # value = value + str(j) + '. '+str(med_dosage_des[0]) + '-----' + str(med_dosage_des[1]) +\
                #         '----' + str(med_dosage_des[2]) + '\n'

            Dict['MEDICINE DOSAGE DESCRIPTION'] = med_dicts_list
            continue
        Dict[key] = value

    print(Dict)
    return Dict


def end_meeting(request, name, appointment_id):
    if 'doctor' not in request.session:
        return redirect(reverse('main_home'))

    doctor = Doctor.objects.get(id=request.session['doctor'])
    appointment = Appointment.objects.get(id=appointment_id)
    patient = appointment.patient
    chamber_id = appointment.chamber_id

    appointment.state = 'Completed'
    appointment.save()

    return redirect(reverse('doctor:show_appointments_chamber', kwargs={'name': doctor.first_name, 'chamber_id': chamber_id}))


def show_completed_appointments(request, name, chamber_id):
    if 'doctor' not in request.session:
        return redirect(reverse('main_home'))

    doctor = Doctor.objects.get(id=request.session['doctor'])
    chamber = Chamber.objects.get(id=chamber_id)
    appointment_list = Appointment.objects.filter(chamber=chamber, state='Completed').order_by('date')
    print('appointment_list')
    print(appointment_list)
    distinct_date = Appointment.objects.filter(chamber=chamber, state='Completed').values('date').distinct()
    print('distimct_date')
    for date in distinct_date:
        print(date)
    dates = []
    date_appmntList_dict = {}
    for data in distinct_date:
        dates.append(str(data['date']))
        description = "some problem. demo problem statement"
        appmntList = []
        dict = {}
        for in_data in appointment_list:
            print("checking print1 " + str(in_data.date))
            print("checking print2 " + str(data['date']))
            if str(in_data.date) == str(data['date']):
                patient = Patient.objects.get(id=in_data.patient.id)
                print("name : " + in_data.patient.first_name + " " + in_data.patient.last_name)
                dict = {
                    'patient': in_data.patient.first_name + " " + in_data.patient.last_name,
                    'patient_id': patient.id,
                    'appointment_id': in_data.id
                }
                appmntList.append(dict)
                dict = {}
        date_appmntList_dict[str(data['date'])] = appmntList
    # print(distinct_date)
    print('date appmnt dict list')
    print(date_appmntList_dict)
    print(dates)
    appointments = []
    for data in appointment_list:
        patient = Patient.objects.get(id=data.patient.id)
        dict = {
            'patient': patient.first_name + " " + patient.last_name,
            'patient_id': patient.id,
            'date': str(data.date)
            # 'dates': dates   # dates in which there are appointment
        }
        print("printing dict")
        print(dict)
        appointments.append(dict)
    print()
    context = {
        'doctor': doctor,
        'chamber': chamber,
        'appointments': date_appmntList_dict,
        'dates': dates  # distinct date list
    }
    print("printing context")
    print(context)
    return render(request, 'Doctor/Appointment/show_completed_appointments.html', context)


def show_completed_prescription(request, name, appointment_id):
    if 'doctor' not in request.session:
        return redirect(reverse('main_home'))

    doctor = Doctor.objects.get(id=request.session['doctor'])
    patient = Appointment.objects.get(id=appointment_id).patient

    context = {
        'Prescription': prescriptionToDict(appointment_id),
        'doctor': doctor,
        'patient': patient,
        'appointment_id': appointment_id
    }

    return render(request, 'Doctor/Appointment/show_completed_prescription.html', context)


def show_patient_appointments(request, name, patient_id):
    if 'doctor' not in request.session:
        return redirect(reverse('main_home'))

    doctor = Doctor.objects.get(id=request.session['doctor'])
    patient = Patient.objects.get(id=patient_id)

    # chambers_of_doctor = Chamber.objects.filter(doctor=doctor)
    # appointment_list = Appointment.objects.filter(patient=patient, state='Completed').order_by('date').values()
    # print('appointment_list')
    # print(appointment_list)
    # app_list = []
    # for app in appointment_list:
    #     checker = False
    #     for chamber in chambers_of_doctor:
    #         if str(chamber.id) == str(app['chamber_id']):
    #             checker = True
    #             app_list.append(app)
    #             break

    app_list = Appointment.objects.filter(patient=patient,chamber__doctor=doctor , state='Completed').order_by('date').values()
    print('app_list')
    print(app_list)

    context = {
        'Appointments': app_list,
        'doctor': doctor,
        'patient': patient
    }

    return render(request, 'Doctor/Appointment/show_completed_appointment_list.html', context)


def start_todays_appointments(request, name, chamber_id):
    if 'doctor' not in request.session:
        return redirect(reverse('main_home'))

    doctor = Doctor.objects.get(id=request.session['doctor'])
    chamber = Chamber.objects.get(id=chamber_id)
    appointments = Appointment.objects.filter(chamber=chamber, state='Requested', date=date.today())

    # cham_appmntlist_list = []
    #
    # for each_chamber in chambers:
    #     dict = { }
    #
    #     list = []
    #     for app in appointments:
    #         if app.chamber_id == each_chamber.id:
    #             list.append(app)
    #
    #     cham_appmntlist_list.append(list)
    #
    # print('cham appmnt list lsit')
    # print(cham_appmntlist_list)
    print('chamer id')
    print(chamber_id)
    print('today date')
    print(str(date.today()))
    print('today appointments')
    print(len(appointments))
    for app in appointments:
        print(str(app.date))

    context = {
        'Appointments': appointments,
        'doctor': doctor,
        'chamber': chamber
    }

    return render(request, 'Doctor/Appointment/todays_appointments.html', context)



# def show_profile_public(request, name, patient_id):
#     if 'doctor' not in request.session:
#         return redirect(reverse('main_home'))
#
#     doctor = Doctor.objects.get(id=request.session['doctor'])
#     patient = Patient.objects.get(id=patient_id)
#
#     context = {
#         'patient': patient
#     }
#
#     return render(request, "Doctor/Appointment/show_patient_public.html", context)
#          error_msg = error_msg + "NO days selected for chamber openings \n"
#
#
        # chamber = Chamber( sat_starttime=sat_start, sat_endtime=sat_end,
        #                   sun_starttime=sun_start, sun_endtime=sun_end,
        #                   mon_starttime=mon_start, mon_endtime=mon_end,
        #                   tues_starttime=tues_start, tues_endtime=tues_end,
        #                   wed_starttime=wed_start, wed_endtime=wed_end,
        #                   thrs_starttime=sat_start, thrs_endtime=sat_end,
        #                   fri_starttime=fri_start, fri_endtime=fri_end,
        #                   address=address, payment=payment
        #                   )
    #     # chamber.save()
    #     return redirect(reverse('doctor:home', kwargs={'name': doctor.first_name}))
    #
    #
    #
    #
    # return render(request, 'Doctor/Chambers/add_chamber.html', context)
    #

# #   text is in format '14:50'
# def convert_time(my_time):
#     TIME = datetime.strptime(my_time, "%H:%M")
#     print(TIME)
#     return TIME

#
# def checkTime(start, end):
#     if start == '' and end == '':
#         return "C"   #"No CHAMBER on this day"
#     elif start == '' and end != '':
#         return "S"   #"START time not defined"
#     elif start != '' and end == '':
#         return "E"     #"END time not defined"
#     else:
#         start = start.split(':')
#         end = end.split(':')
#         startInMinutes = int(start[0])*60 + int(start[1])
#         endInMinutes = int(end[0])*60 + int(end[1])
#
#         #   doctor is sitting for AT LEAST >0 minutes today
#         if endInMinutes - startInMinutes > 0:
#             return "V"  #VALID
#         else:
#             return "N"  #NOT VALID #START TIME > END TIME

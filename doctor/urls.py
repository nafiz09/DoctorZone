from django.contrib import admin
from django.urls import path, include
import patient.views
from django.views.generic import TemplateView
import doctor.views as doctor_views

app_name = 'doctor'

urlpatterns = [
    path('signup/', doctor_views.signup, name='doctor_signup'),
    path('<slug:name>/', doctor_views.load_doctor_rev, name='home'),
    path('<slug:name>/add_chamber/', doctor_views.add_chamber, name='add_chamber'),
    path('<slug:name>/show_chamber/', doctor_views.show_chamber, name='show_chamber'),
    path('<slug:name>/edit_chamber/<slug:chamber_id>/', doctor_views.edit_chamber, name='edit_chamber'),
    path('<slug:name>/show_appointments/chamber/<slug:chamber_id>/', doctor_views.show_appointments_chamber, name='show_appointments_chamber'),
    path('<slug:name>/customize_prescription/', doctor_views.customize_prescription, name='customize_prescription'),
    path('<slug:name>/show_profile/', doctor_views.show_profile, name='show_profile'),
    path('<slug:name>/show_patient_profile/<slug:patient_id>/', doctor_views.show_patient_profile, name='show_patient_profile'),
    path('<slug:name>/write_prescription/<slug:appointment_id>/', doctor_views.write_prescription, name='write_prescription'),
    path('<slug:name>/OTP/<slug:appointment_id>/', doctor_views.input_OTP, name='input_OTP'),
    path('<slug:name>/end_meeting/<slug:appointment_id>/', doctor_views.end_meeting, name='end_meeting'),
    path('<slug:name>/show_completed_appointments/<slug:chamber_id>/', doctor_views.show_completed_appointments, name='show_completed_appointments'),
    path('<slug:name>/show_prescription/<slug:appointment_id>/', doctor_views.show_completed_prescription, name='show_completed_prescription'),
    path('<slug:name>/show_patient_appointments/<slug:patient_id>/', doctor_views.show_patient_appointments, name='show_patient_appointments'),
    path('<slug:name>/start_todays_appointments/<slug:chamber_id>/', doctor_views.start_todays_appointments, name='start_todays_appointment')

    # path('', doctor_views.load_doctor, name='doctor_home')

]

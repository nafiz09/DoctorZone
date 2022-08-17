from django.contrib import admin
from django.urls import path, include
import patient.views
from django.views.generic import TemplateView
import doctor.views as doctor_views

app_name = 'doctor'

urlpatterns = [
    path('signup/', doctor_views.signup, name='doctor_signup'),
    path('<slug:name>/', doctor_views.load_doctor_rev, name='home'),
    # path('logout/', doctor_views.delete_session, name='logout')

    path('<slug:name>/add_chamber/', doctor_views.add_chamber, name='add_chamber'),
    path('<slug:name>/show_chamber/', doctor_views.show_chamber, name='show_chamber'),
    path('<slug:name>/edit_chamber/<slug:chamber_id>/', doctor_views.edit_chamber, name='edit_chamber'),
    # path('<slug:name>/show_appointments/chamber/', doctor_views.show_appointments_chamber, name='show_appointments_chamber')
    path('<slug:name>/show_appointments/chamber/<slug:chamber_id>', doctor_views.show_appointments_chamber, name='show_appointments_chamber'),

    path('<slug:name>/customize_prescription/', doctor_views.customize_prescription, name='prescription'),
    # path('', doctor_views.load_doctor, name='doctor_home')

    # path('<slug:name>/show_profile_public/<slug:patient_id>/', doctor_views.show_profile_public, name='show_profile_public')


    # path('', doctor_views.load_doctor, name='doctor_home')

]

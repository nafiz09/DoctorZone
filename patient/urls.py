from django.contrib import admin
from django.urls import path
import patient.views as patient_views
from django.views.generic import TemplateView
app_name = 'patient'

urlpatterns = [
    path('<slug:name>/Pharmacy/', patient_views.show_products, name='show_products'),
    path('pharmacy-info/', patient_views.test_function, name='show-pharmacy-info'),
    path('signup/', patient_views.signup, name='patient_signup'),
    path('<slug:name>/', patient_views.load_patient, name='home'),
    path('<slug:name>/search_result/', patient_views.search_result, name='search_result'),
    path('<slug:name>/take_appointment/<slug:chamber_id>/', patient_views.take_appointment, name='take_appointment'),
    path('<slug:name>/show_appointments/', patient_views.show_appointments, name='show_appointments'),
    path('<slug:name>/', patient_views.load_patient, name='home'),
    path('<slug:name>/show_doc_profile/<slug:chamber_id>/', patient_views.show_doctor_profile,name = 'show_doctor_profile'),
    path('<slug:name>/show_profile/', patient_views.show_profile, name='show_profile'),
    path('<slug:name>/show_prescription/<slug:appointment_id>/', patient_views.show_prescription, name='show_prescription')
]

from django.contrib import admin
from django.urls import path
import patient.views as patient_views
from django.views.generic import TemplateView
app_name = 'patient'

urlpatterns = [
    path('signup/', patient_views.signup, name='patient_signup'),
    # path('', patient_views.load_patient, name='home'),
    path('Pharmacy/', patient_views.show_products, name='show_products'),
    path('<slug:name>/', patient_views.load_patient, name='home')
]
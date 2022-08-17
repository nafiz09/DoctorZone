from django.contrib import admin
from django.urls import path
import patient.views
from django.views.generic import TemplateView
import doctor.views as doctor_views

app_name = 'doctor'

urlpatterns = [
    path('signup/', doctor_views.signup, name='doctor_signup'),
    path('<slug:name>/', doctor_views.load_doctor_rev, name='home'),
    # path('logout/', doctor_views.delete_session, name='logout')
    path('<slug:name>/add_chamber/', doctor_views.add_chamber, name='add_chamber')

    # path('', doctor_views.load_doctor, name='doctor_home')
]

from django.contrib import admin
from django.urls import path
import patient.views as patient_views
from django.views.generic import TemplateView
app_name = 'patient'

urlpatterns = [
    path('signup/', patient_views.signup, name='patient_signup'),
    # path('', patient_views.load_patient, name='home'),
    path('<slug:name>/', patient_views.load_patient, name='home'),
    path('<slug:name>/search_result/', patient_views.search_result, name='search_result'),
    path('<slug:name>/take_appointment/<slug:chamber_id>/', patient_views.take_appointment, name='take_appointment'),
    path('<slug:name>/show_appointments/', patient_views.show_appointments, name='show_appointments'),
    # path('show_profile_public/<slug:patient_id>/'), patient_views.show_profile_public, name='show_profile_public')
    path('<slug:name>/edit_profile/', patient_views.edit_profile, name='edit_profile'),
    path('<slug:name>/show_profile/', patient_views.show_profile, name='show_profile')
]
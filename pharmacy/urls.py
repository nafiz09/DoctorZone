from django.contrib import admin
from django.urls import path
import pharmacy.views as pharmacy_views
from django.views.generic import TemplateView
app_name = 'pharmacy'

urlpatterns = [
    path('signup/', pharmacy_views.signup, name='pharmacy_signup'),
    # path('', patient_views.load_patient, name='home'),
    path('add_product/', pharmacy_views.add_product, name='add_product'),
    path('show_products/', pharmacy_views.show_products, name='show_products'),
    path('<slug:name>/', pharmacy_views.load_pharmacy, name='home')
]
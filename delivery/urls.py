from django.contrib import admin
from django.urls import path
import delivery.views as delivery_views
from django.views.generic import TemplateView
app_name = 'delivery'

urlpatterns = [
    path('signup/', delivery_views.signup, name='signup')

    # path('', patient_views.load_patient, name='home'),
    # path('add_product/', pharmacy_views.add_product, name='add_product'),
    # path('show_products/', pharmacy_views.show_products, name='show_products'),
    # path('<slug:name>/', delivery_views.load_delivery, name='home')
]
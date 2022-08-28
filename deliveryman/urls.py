from django.contrib import admin
from django.urls import path
import deliveryman.views as deliveryman_views
from django.views.generic import TemplateView
app_name = 'deliveryman'

urlpatterns = [
    path('signup/', deliveryman_views.signup, name='deliveryman_signup'),
    path('pending/', deliveryman_views.pending_orders, name='pending_orders'),
    path('running/', deliveryman_views.running_orders, name='running_orders'),
    path('deliverd/', deliveryman_views.completed_orders, name='completed_orders'),
    path('<slug:name>/', deliveryman_views.load_deliveryman, name='home')
]
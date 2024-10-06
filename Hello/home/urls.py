from django.contrib import admin
from django.urls import path
from home import views
from . import views
admin.site.site_header = "Finology Admin"
admin.site.site_title = "Finology Admin Portal"
admin.site.index_title = "Welcome to Finology Researcher Portal"

urlpatterns = [
    path('', views.index, name='home' ),
    path('about/', views.about, name='about'),
    path('services/', views.services, name='services'),
    path('contact/', views.contact, name='contact'),
    path('admin/', admin.site.urls),
    path('investment_plan/', views.investment_plan, name='investment_plan'),
    path('tax_calculator/', views.tax_calculator, name="tax_calculator") 
 
    ]

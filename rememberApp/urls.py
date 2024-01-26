from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("about_us/", views.about, name="about"),
    path("services/", views.services, name="services"),
    path("service-detail/<int:pk>/", views.service_details, name="service_detail"),
    path('feedback/', views.feedback, name='feedback'),
    path('contact/', views.contact, name='contact'),
    ]

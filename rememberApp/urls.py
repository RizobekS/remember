from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='registration'),
    path('logout-user/', views.logout_view, name='logout-user'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path("", views.home, name="home"),
    path("about_us/", views.about, name="about"),
    path("cemeteries/", views.cemeteries, name="cemeteries"),
    path("cemetery-detail/<int:pk>/", views.cemetery_details, name="cemetery_details"),
    path("services/", views.services, name="services"),
    path("service-detail/<int:pk>/", views.service_details, name="service_detail"),
    path('feedback/', views.feedback, name='feedback'),
    path('contact/', views.contact, name='contact'),
    path('gallery/', views.gallery, name='gallery'),
    path('click_generate_url/<int:amount>/<int:service_id>/', views.click_generate_url, name='click_generate_url'),
    path('payme_generate_url/', views.payme_generate_url, name='payme_generate_url'),
    path('success_payment', views.payment_success, name='success_payment'),
    path('invoice/<int:id>/', views.invoice, name='invoice'),
    path('myservice-detail/<int:id>/', views.myservicedetail, name='myservice-detail'),

]

from django.urls import path
from django.views.generic.base import RedirectView
from transaction import views

urlpatterns = [
    path("payments/merchant/", views.PaymeCallBackAPIView.as_view()),
    path(
        "integration_with_click/",
        view=views.accept_click_request_view,
        name="accept_click_requests",
    ),

    path('click/transaction/', views.OrderTestView.as_view()),
]

from django.urls import path

from . import views

urlpatterns = [
    path('', views.exchange, name='exchange'),
    path('thank-you/', views.thankyou, name='thankyou'),
]

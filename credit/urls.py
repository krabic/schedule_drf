from django.urls import path

from .update_payment_schedule_views import PaymentScheduleUpdateView
from .create_payment_schedule_views import PaymentScheduleCreateView
"""
http://127.0.0.1:8000/api/credit/create-payment-schedule/

http://127.0.0.1:8000/api/credit/update-payment-schedule/
"""
urlpatterns = [

    path('create-payment-schedule/', PaymentScheduleCreateView.as_view(http_method_names=['post']),
         name='create-payment-schedule'),
    path('update-payment-schedule/', PaymentScheduleUpdateView.as_view(http_method_names=['post']),
         name='update-payment-schedule'),
]

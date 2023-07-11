from django.urls import path

from .update_payment_schedule_views import PaymentScheduleUpdateView
from .create_payment_schedule_views import PaymentScheduleCreateView

urlpatterns = [

    path('create-payment-schedule/', PaymentScheduleCreateView.as_view(http_method_names=['post']),
         name='create-payment-schedule'),
    path('update-payment-schedule/', PaymentScheduleUpdateView.as_view(http_method_names=['post']),
         name='update-payment-schedule'),
]

from django.core.exceptions import ObjectDoesNotExist
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import PaymentSchedule, Payment
from .serializers import PaymentUpdateSerializer
from datetime import timedelta
from calendar import monthrange


class PaymentScheduleUpdateView(APIView):
    """View for updating payment schedules."""

    @staticmethod
    def post(request):
        """
        Handle POST request to update a payment schedule.

        Args:
            request (HttpRequest): The HTTP request object.

        Returns:
            Response: HTTP response indicating the status of the request.

        Payload example:
        { "payment_id": 1, "principal_reduction": 500 }
        """

        serializer = PaymentUpdateSerializer(data=request.data)
        if serializer.is_valid():
            payment_id = serializer.validated_data['payment_id']
            principal_reduction = serializer.validated_data['principal_reduction']
            try:
                payment_schedule = PaymentSchedule.objects.get(id=payment_id)
                payment = payment_schedule.payment
                payment.principal -= principal_reduction
                payment.save()

                # Recalculate interest for the current payment
                interest_rate_per_period = payment_schedule.interest_rate / 12
                interest_payment = payment.principal * interest_rate_per_period
                payment.interest = interest_payment
                payment.save()

                # Recalculate interest for the following payments
                following_payments = Payment.objects.filter(paymentschedule__id__gt=payment_schedule.id)

                principal_remaining = payment_schedule.amount - payment.principal
                if payment_schedule.periodicity.endswith('d'):  # Daily
                    delta = timedelta(days=int(payment_schedule.periodicity[:-1]))
                elif payment_schedule.periodicity.endswith('w'):  # Weekly
                    delta = timedelta(weeks=int(payment_schedule.periodicity[:-1]))
                else:  # Monthly
                    current_date = payment_schedule.loan_start_date
                    days_in_month = monthrange(current_date.year, current_date.month)[1]
                    delta = timedelta(days=days_in_month)

                for following_payment in following_payments:
                    interest_payment = principal_remaining * interest_rate_per_period
                    following_payment.interest = interest_payment
                    following_payment.save()
                    principal_remaining -= following_payment.principal

                    payment_schedule.loan_start_date += delta
                    payment_schedule.save()

                return Response(status=status.HTTP_200_OK)

            except ObjectDoesNotExist:
                return Response("Payment not found", status=status.HTTP_404_NOT_FOUND)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

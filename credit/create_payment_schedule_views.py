from datetime import timedelta
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import PaymentSchedule, Payment
from .serializers import PaymentScheduleSerializer


class PaymentScheduleCreateView(APIView):
    """
    API view for creating a payment schedule.

    POST request with the payment details will generate a payment schedule
    and store it in the database.

    Returns:
        Response: Created payment schedule in JSON format or error messages.
    """

    @staticmethod
    def post(request):
        """
        Handle POST request to create a payment schedule.

        Args:
            request (Request): HTTP request object containing payment details.

        Returns:
            Response: Created payment schedule in JSON format or error messages.

        Payload example:
        { "amount": 10000, "loan_start_date": "2023-07-10", "number_of_payments": 12, "periodicity": "1m", "interest_rate": 5 }
        """
        serializer = PaymentScheduleSerializer(data=request.data)
        if serializer.is_valid():
            amount = serializer.validated_data['amount']
            loan_start_date = serializer.validated_data['loan_start_date']
            number_of_payments = serializer.validated_data['number_of_payments']
            periodicity = serializer.validated_data['periodicity']
            interest_rate = serializer.validated_data['interest_rate']

            # Perform calculations to generate the payment schedule based on the provided data
            interest_rate_per_period = interest_rate / 12  # Assuming interest rate is given as an annual rate
            emi = (interest_rate_per_period * amount) / (1 - (1 + interest_rate_per_period) ** -number_of_payments)

            payment_schedule = []
            principal_remaining = amount
            payment_date = loan_start_date
            delta = timedelta(days=0)
            if periodicity.endswith('m'):  # Monthly
                delta = timedelta(days=30 * int(periodicity[:-1]))
            elif periodicity.endswith('w'):  # Weekly
                delta = timedelta(weeks=int(periodicity[:-1]))
            elif periodicity.endswith('d'):  # Daily
                delta = timedelta(days=int(periodicity[:-1]))

            for payment_number in range(1, number_of_payments + 1):
                interest_payment = principal_remaining * interest_rate_per_period
                principal_payment = emi - interest_payment
                principal_remaining -= principal_payment

                payment_schedule.append({
                    'id': payment_number,
                    'date': payment_date.strftime('%Y-%m-%d'),
                    'principal': principal_payment,
                    'interest': interest_payment
                })

                payment_date += delta

            payment_objects = [
                Payment(date=payment['date'], principal=payment['principal'], interest=payment['interest'])
                for payment in payment_schedule
            ]
            Payment.objects.bulk_create(payment_objects)
            payment_schedule_objects = [
                PaymentSchedule(amount=amount, loan_start_date=loan_start_date, number_of_payments=number_of_payments,
                                periodicity=periodicity, interest_rate=interest_rate, payment=payment)
                for payment, schedule in zip(payment_objects, payment_schedule)
            ]
            PaymentSchedule.objects.bulk_create(payment_schedule_objects)

            # Return the response with the created payment schedule in JSON format
            return Response(payment_schedule, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

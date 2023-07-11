from rest_framework import serializers
from .models import Payment, PaymentSchedule


class PaymentScheduleSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentSchedule
        fields = ['id', 'amount', 'loan_start_date', 'number_of_payments', 'periodicity', 'interest_rate']


class PaymentSerializer(serializers.ModelSerializer):
    payment_schedule = PaymentScheduleSerializer()

    class Meta:
        model = Payment
        fields = ['id', 'date', 'principle', 'interest']


class PaymentUpdateSerializer(serializers.Serializer):
    payment_id = serializers.IntegerField()
    principal_reduction = serializers.DecimalField(max_digits=10, decimal_places=2)

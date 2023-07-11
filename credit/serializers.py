from rest_framework import serializers
from .models import Payment, PaymentSchedule


class PaymentScheduleSerializer(serializers.ModelSerializer):
    """
    Serializer for the PaymentSchedule model.
    """

    class Meta:
        model = PaymentSchedule
        fields = ['id', 'amount', 'loan_start_date', 'number_of_payments', 'periodicity', 'interest_rate']


class PaymentSerializer(serializers.ModelSerializer):
    """
    Serializer for the Payment model.
    """

    payment_schedule = PaymentScheduleSerializer()

    class Meta:
        model = Payment
        fields = ['id', 'date', 'principle', 'interest']


class PaymentUpdateSerializer(serializers.Serializer):
    """
    Serializer for updating Payment instances.
    """

    payment_id = serializers.IntegerField()
    principal_reduction = serializers.DecimalField(max_digits=10, decimal_places=2)

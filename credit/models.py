from django.db import models


class PaymentScheduleManager(models.Manager):
    pass


class Payment(models.Model):
    date = models.DateField()
    principal = models.DecimalField(max_digits=10, decimal_places=2)
    interest = models.DecimalField(max_digits=10, decimal_places=2)

    objects = PaymentScheduleManager()


class PaymentSchedule(models.Model):
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    loan_start_date = models.DateField()
    number_of_payments = models.IntegerField()
    periodicity = models.CharField(max_length=10)
    interest_rate = models.DecimalField(max_digits=4, decimal_places=2)
    payment = models.ForeignKey(Payment, on_delete=models.CASCADE, null=True)

    objects = PaymentScheduleManager()

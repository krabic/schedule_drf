# Generated by Django 4.2.3 on 2023-07-10 23:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('credit', '0002_remove_paymentschedule_payment_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='payment',
            name='payment_schedule',
        ),
        migrations.AddField(
            model_name='paymentschedule',
            name='payment',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='credit.payment'),
        ),
    ]

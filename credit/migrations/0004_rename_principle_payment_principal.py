# Generated by Django 4.2.3 on 2023-07-11 00:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('credit', '0003_remove_payment_payment_schedule_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='payment',
            old_name='principle',
            new_name='principal',
        ),
    ]
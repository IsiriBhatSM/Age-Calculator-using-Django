# Generated by Django 5.0.6 on 2024-08-04 14:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('calculator', '0003_dob_is_future_date'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='dob',
            name='is_future_date',
        ),
    ]

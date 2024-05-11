# Generated by Django 5.0.4 on 2024-05-11 13:07

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('factory', '0002_client_user_employee_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='client',
            name='phone',
            field=models.CharField(max_length=20, validators=[django.core.validators.RegexValidator(message="Phone number must be entered in the format: '+375 (XX) XXX-XX-XX'. Up to 9 digits allowed.", regex='^\\+375 \\(\\d{2}\\) \\d{3}-\\d{2}-\\d{2}$')]),
        ),
        migrations.AlterField(
            model_name='employee',
            name='phone',
            field=models.CharField(max_length=20, validators=[django.core.validators.RegexValidator(message="Phone number must be entered in the format: '+375 (XX) XXX-XX-XX'. Up to 9 digits allowed.", regex='^\\+375 \\(\\d{2}\\) \\d{3}-\\d{2}-\\d{2}$')]),
        ),
    ]
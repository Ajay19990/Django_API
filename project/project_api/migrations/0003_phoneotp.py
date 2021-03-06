# Generated by Django 3.1 on 2020-08-14 14:20

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project_api', '0002_userprofile_phone'),
    ]

    operations = [
        migrations.CreateModel(
            name='PhoneOTP',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phone', models.CharField(max_length=17, unique=True, validators=[django.core.validators.RegexValidator(message='Phone number must be entered in proper format.', regex='^\\+?1?\\d{9,14$')])),
                ('otp', models.CharField(blank=True, max_length=9, null=True)),
                ('count', models.IntegerField(default=0, help_text='Number of otp sent')),
            ],
        ),
    ]

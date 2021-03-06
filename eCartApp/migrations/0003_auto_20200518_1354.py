# Generated by Django 3.0.6 on 2020-05-18 17:54

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('eCartApp', '0002_auto_20200518_1001'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='username',
            field=models.CharField(max_length=50, validators=[django.core.validators.RegexValidator('^[0-9a-zA-Z]*$', 'Username can only contain alphanumeric characters.')]),
        ),
        migrations.AlterField(
            model_name='vendor',
            name='vendor_name',
            field=models.CharField(max_length=50, validators=[django.core.validators.RegexValidator('^[0-9a-zA-Z]*$', 'Username can only contain alphanumeric characters.')]),
        ),
    ]

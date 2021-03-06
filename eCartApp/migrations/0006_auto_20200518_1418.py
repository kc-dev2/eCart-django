# Generated by Django 3.0.6 on 2020-05-18 18:18

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('eCartApp', '0005_auto_20200518_1416'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='prod_name',
            field=models.CharField(max_length=100, validators=[django.core.validators.RegexValidator('^\\w+( \\w+)*$', 'Product name can only contain alphanumeric characters and cannot start/end with whitespace.')]),
        ),
    ]

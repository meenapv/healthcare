# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0004_billing'),
    ]

    operations = [
        migrations.AlterField(
            model_name='billing',
            name='amount',
            field=models.FloatField(max_length=50),
        ),
        migrations.AlterField(
            model_name='billing',
            name='status',
            field=models.CharField(max_length=100),
        ),
    ]

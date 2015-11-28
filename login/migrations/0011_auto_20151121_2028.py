# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0010_auto_20151121_2024'),
    ]

    operations = [
        migrations.AlterField(
            model_name='leave',
            name='current_year',
            field=models.IntegerField(default=2015),
        ),
        migrations.AlterField(
            model_name='leave',
            name='leave_limit',
            field=models.IntegerField(default=6),
        ),
    ]

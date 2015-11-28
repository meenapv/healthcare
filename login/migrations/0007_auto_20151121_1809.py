# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0006_auto_20151121_1742'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='leave',
            name='current_year',
        ),
        migrations.RemoveField(
            model_name='leave',
            name='leave_limit',
        ),
    ]

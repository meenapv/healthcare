# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0009_document'),
    ]

    operations = [
        migrations.AddField(
            model_name='leave',
            name='current_year',
            field=models.IntegerField(default=2015),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='leave',
            name='leave_limit',
            field=models.IntegerField(default=6),
            preserve_default=False,
        ),
    ]

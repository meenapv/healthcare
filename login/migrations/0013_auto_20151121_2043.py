# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0012_remove_leave_current_year'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='leave',
            name='doctor',
        ),
        migrations.DeleteModel(
            name='Leave',
        ),
    ]

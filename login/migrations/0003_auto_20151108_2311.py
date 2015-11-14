# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('login', '0002_appt'),
    ]

    operations = [
        migrations.RenameField(
            model_name='appt',
            old_name='doctor_name',
            new_name='prescription',
        ),
        migrations.RemoveField(
            model_name='appt',
            name='patient_user',
        ),
        migrations.RemoveField(
            model_name='appt',
            name='uname',
        ),
        migrations.AddField(
            model_name='appt',
            name='doctor',
            field=models.ForeignKey(related_name='doctor_user', to=settings.AUTH_USER_MODEL, null=True),
        ),
        migrations.AddField(
            model_name='appt',
            name='patient',
            field=models.ForeignKey(related_name='patient_user', to=settings.AUTH_USER_MODEL, null=True),
        ),
    ]

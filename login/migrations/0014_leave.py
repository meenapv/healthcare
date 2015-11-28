# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('login', '0013_auto_20151121_2043'),
    ]

    operations = [
        migrations.CreateModel(
            name='Leave',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('reason', models.CharField(max_length=100)),
                ('date_of_leave', models.DateField()),
                ('current_year', models.IntegerField(default=1111)),
                ('leave_limit', models.IntegerField(default=6)),
                ('status', models.CharField(max_length=30)),
                ('doctor', models.ForeignKey(related_name='doctor', to=settings.AUTH_USER_MODEL, null=True)),
            ],
        ),
    ]

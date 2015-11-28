# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('login', '0005_auto_20151109_0026'),
    ]

    operations = [
        migrations.CreateModel(
            name='Document',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('docfile', models.FileField(upload_to=b'documents/')),
            ],
        ),
        migrations.CreateModel(
            name='Leave',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('reason', models.CharField(max_length=100)),
                ('date_of_leave', models.DateField()),
                ('current_year', models.IntegerField(max_length=4)),
                ('leave_limit', models.IntegerField(max_length=2)),
                ('status', models.CharField(max_length=30)),
                ('doctor', models.ForeignKey(related_name='doctor', to=settings.AUTH_USER_MODEL, null=True)),
            ],
        ),
        migrations.AlterField(
            model_name='userrole',
            name='role',
            field=models.CharField(max_length=10, choices=[(b'Patient', b'Patient'), (b'Doctor', b'Doctor'), (b'Staff', b'Staff'), (b'Admin', b'Admin')]),
        ),
    ]

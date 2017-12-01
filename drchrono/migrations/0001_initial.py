# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Appointment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('appointment_id', models.CharField(max_length=100)),
                ('scheduled_time', models.DateTimeField()),
                ('duration', models.TimeField(max_length=10)),
                ('patient_id', models.CharField(max_length=100)),
                ('patient_SSN', models.CharField(max_length=100)),
                ('patient_first_name', models.CharField(max_length=100)),
                ('patient_last_name', models.CharField(max_length=100)),
                ('arrived_time', models.DateTimeField(blank=True)),
                ('waiting_time', models.TimeField(blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Doctor',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('user_id', models.IntegerField(max_length=100)),
                ('user', models.CharField(max_length=100)),
                ('average_waiting_time', models.IntegerField(default=5)),
            ],
        ),
        migrations.AddField(
            model_name='appointment',
            name='doctor_id',
            field=models.ForeignKey(to='drchrono.Doctor'),
        ),
    ]

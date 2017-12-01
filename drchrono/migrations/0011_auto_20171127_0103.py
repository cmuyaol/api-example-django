# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('drchrono', '0010_auto_20171122_2135'),
    ]

    operations = [
        migrations.AlterField(
            model_name='appointment',
            name='scheduled_time',
            field=models.DateTimeField(default=datetime.datetime(2017, 11, 27, 1, 3, 56, 677226, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='appointment',
            name='waiting_time',
            field=models.DateTimeField(null=True),
        ),
    ]

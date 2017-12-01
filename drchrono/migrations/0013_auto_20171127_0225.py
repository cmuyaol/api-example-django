# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('drchrono', '0012_auto_20171127_0104'),
    ]

    operations = [
        migrations.AlterField(
            model_name='appointment',
            name='scheduled_time',
            field=models.DateTimeField(default=datetime.datetime(2017, 11, 27, 2, 25, 21, 236041, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='appointment',
            name='waiting_time',
            field=models.IntegerField(null=True),
        ),
    ]

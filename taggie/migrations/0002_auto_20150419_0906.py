# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('taggie', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='sticker',
            name='pub_date',
            field=models.DateTimeField(default=datetime.date(2015, 4, 19), verbose_name=b'date added', auto_now_add=True),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='sticker',
            name='like',
            field=models.IntegerField(default=0),
        ),
    ]

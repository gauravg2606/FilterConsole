# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('taggie', '0014_auto_20150505_1100'),
    ]

    operations = [
        migrations.AddField(
            model_name='tag',
            name='lang',
            field=models.CharField(default=b'english', max_length=20),
            preserve_default=True,
        ),
    ]

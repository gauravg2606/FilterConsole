# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('taggie', '0012_auto_20150420_1632'),
    ]

    operations = [
        migrations.AddField(
            model_name='tag',
            name='theme',
            field=models.CharField(default=None, max_length=20),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='tag',
            name='name',
            field=models.CharField(max_length=30),
        ),
    ]

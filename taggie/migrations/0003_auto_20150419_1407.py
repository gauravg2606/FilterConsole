# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('taggie', '0002_auto_20150419_0906'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='tag',
            name='votes',
        ),
        migrations.AddField(
            model_name='tag',
            name='downvotes',
            field=models.IntegerField(default=0),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='tag',
            name='upvotes',
            field=models.IntegerField(default=0),
            preserve_default=True,
        ),
    ]

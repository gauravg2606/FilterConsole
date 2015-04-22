# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('taggie', '0008_auto_20150420_1409'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='tag',
            name='behaviour',
        ),
        migrations.RemoveField(
            model_name='tag',
            name='emotion',
        ),
        migrations.RemoveField(
            model_name='tag',
            name='feeling',
        ),
        migrations.RemoveField(
            model_name='tag',
            name='general',
        ),
        migrations.RemoveField(
            model_name='tag',
            name='other',
        ),
        migrations.RemoveField(
            model_name='tag',
            name='reaction',
        ),
        migrations.RemoveField(
            model_name='tag',
            name='regional',
        ),
        migrations.RemoveField(
            model_name='tag',
            name='response',
        ),
        migrations.RemoveField(
            model_name='tag',
            name='smiley',
        ),
        migrations.RemoveField(
            model_name='tag',
            name='theme',
        ),
        migrations.RemoveField(
            model_name='tagtheme',
            name='behaviour',
        ),
        migrations.RemoveField(
            model_name='tagtheme',
            name='emotion',
        ),
        migrations.RemoveField(
            model_name='tagtheme',
            name='feeling',
        ),
        migrations.RemoveField(
            model_name='tagtheme',
            name='general',
        ),
        migrations.RemoveField(
            model_name='tagtheme',
            name='other',
        ),
        migrations.RemoveField(
            model_name='tagtheme',
            name='reaction',
        ),
        migrations.RemoveField(
            model_name='tagtheme',
            name='regional',
        ),
        migrations.RemoveField(
            model_name='tagtheme',
            name='response',
        ),
        migrations.RemoveField(
            model_name='tagtheme',
            name='smiley',
        ),
        migrations.RemoveField(
            model_name='tagtheme',
            name='theme',
        ),
        migrations.AddField(
            model_name='tagtheme',
            name='name',
            field=models.CharField(default='jim', max_length=20),
            preserve_default=False,
        ),
    ]

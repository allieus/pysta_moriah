# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('timeline', '0005_auto_20150508_1457'),
        ('member', '0002_profile_follower'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='timeline',
            field=models.ManyToManyField(related_name='reader', to='timeline.Post'),
            preserve_default=True,
        ),
    ]

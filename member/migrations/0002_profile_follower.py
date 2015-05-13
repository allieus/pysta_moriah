# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('member', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='follower',
            field=models.ManyToManyField(related_name='following', to='member.Profile'),
            preserve_default=True,
        ),
    ]

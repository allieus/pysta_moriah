# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('timeline', '0004_comment'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='owner',
            field=models.ForeignKey(related_name='comments', to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='post',
            name='image',
            field=models.CharField(max_length=128),
            preserve_default=True,
        ),
    ]

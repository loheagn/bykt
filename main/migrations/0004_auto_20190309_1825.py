# -*- coding: utf-8 -*-
# Generated by Django 1.11.8 on 2019-03-09 18:25
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_auto_20190309_1800'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='student',
            name='email',
        ),
        migrations.RemoveField(
            model_name='student',
            name='face_image',
        ),
    ]

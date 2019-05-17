# -*- coding: utf-8 -*-
# Generated by Django 1.11.8 on 2019-03-10 16:23
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0008_article'),
    ]

    operations = [
        migrations.CreateModel(
            name='VisitImage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(unique=True, upload_to='images/visit')),
                ('is_ok', models.BooleanField()),
                ('similar', models.FloatField()),
                ('v_time', models.DateField()),
                ('location', models.CharField(max_length=256)),
                ('c_time', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.AddField(
            model_name='student',
            name='my_article',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='student',
            name='sport',
            field=models.FloatField(default=0.0),
        ),
        migrations.AddField(
            model_name='student',
            name='visit',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='student',
            name='volunteer',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='visitimage',
            name='student',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.Student'),
        ),
    ]

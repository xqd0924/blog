# -*- coding: utf-8 -*-
# Generated by Django 1.11.9 on 2018-11-29 04:05
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0003_auto_20181128_1023'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='userinfo',
            options={'verbose_name': '用户表', 'verbose_name_plural': '用户表'},
        ),
        migrations.AddField(
            model_name='article',
            name='commit_num',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='article',
            name='down_num',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='article',
            name='up_num',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='article',
            name='title',
            field=models.CharField(max_length=64, verbose_name='文章标题'),
        ),
        migrations.AlterField(
            model_name='commit',
            name='parent',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='blog.Commit'),
        ),
        migrations.AlterField(
            model_name='userinfo',
            name='phone',
            field=models.CharField(blank=True, max_length=32, null=True),
        ),
    ]

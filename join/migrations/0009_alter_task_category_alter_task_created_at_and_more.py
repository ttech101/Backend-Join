# Generated by Django 5.0 on 2023-12-22 07:23

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('join', '0008_alter_task_subtasks'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='category',
            field=models.JSONField(null=True),
        ),
        migrations.AlterField(
            model_name='task',
            name='created_at',
            field=models.DateField(default=datetime.date.today, null=True),
        ),
        migrations.AlterField(
            model_name='task',
            name='date',
            field=models.CharField(max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='task',
            name='headline',
            field=models.CharField(max_length=150, null=True),
        ),
        migrations.AlterField(
            model_name='task',
            name='idBox',
            field=models.CharField(max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name='task',
            name='priority',
            field=models.CharField(max_length=30, null=True),
        ),
        migrations.AlterField(
            model_name='task',
            name='task_board',
            field=models.CharField(max_length=40, null=True),
        ),
        migrations.AlterField(
            model_name='task',
            name='task_user',
            field=models.JSONField(null=True),
        ),
        migrations.AlterField(
            model_name='task',
            name='text',
            field=models.CharField(max_length=500, null=True),
        ),
    ]
# Generated by Django 5.0 on 2023-12-21 15:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('join', '0007_alter_task_idbox'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='subtasks',
            field=models.JSONField(null=True),
        ),
    ]

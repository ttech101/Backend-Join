# Generated by Django 5.0 on 2023-12-21 07:15

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('join', '0007_contact_created_at_task'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contact',
            name='created_at',
            field=models.DateField(default=datetime.date(2023, 12, 21)),
        ),
        migrations.AlterField(
            model_name='task',
            name='created_at',
            field=models.DateField(default=datetime.date(2023, 12, 21)),
        ),
    ]

# Generated by Django 5.0 on 2023-12-21 13:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('join', '0003_alter_contact_phone_number'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contact',
            name='phone_number',
            field=models.CharField(max_length=20),
        ),
    ]

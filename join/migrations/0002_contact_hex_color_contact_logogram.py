# Generated by Django 5.0 on 2023-12-21 10:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('join', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='contact',
            name='hex_color',
            field=models.CharField(default='abc', max_length=10),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='contact',
            name='logogram',
            field=models.CharField(default='abc', max_length=5),
            preserve_default=False,
        ),
    ]

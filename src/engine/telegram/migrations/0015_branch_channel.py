# Generated by Django 2.2.4 on 2020-07-22 17:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('telegram', '0014_auto_20200720_1733'),
    ]

    operations = [
        migrations.AddField(
            model_name='branch',
            name='channel',
            field=models.BigIntegerField(default=0, verbose_name='Channel Id'),
        ),
    ]

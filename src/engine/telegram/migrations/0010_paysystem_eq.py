# Generated by Django 2.2.4 on 2020-07-19 20:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('telegram', '0009_paysystem_currency'),
    ]

    operations = [
        migrations.AddField(
            model_name='paysystem',
            name='eq',
            field=models.IntegerField(default=100, verbose_name='PaySystem Equalizer'),
        ),
    ]

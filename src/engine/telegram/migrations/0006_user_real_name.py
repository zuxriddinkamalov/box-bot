# Generated by Django 2.2.4 on 2020-07-15 10:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('telegram', '0005_auto_20200712_0026'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='real_name',
            field=models.CharField(blank=True, default=None, max_length=255, null=True, verbose_name='Last Name'),
        ),
    ]

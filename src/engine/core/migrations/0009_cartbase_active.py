# Generated by Django 2.2.4 on 2020-07-14 11:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0008_merge_20200714_1640'),
    ]

    operations = [
        migrations.AddField(
            model_name='cartbase',
            name='active',
            field=models.BooleanField(default=True, verbose_name='Active'),
        ),
    ]

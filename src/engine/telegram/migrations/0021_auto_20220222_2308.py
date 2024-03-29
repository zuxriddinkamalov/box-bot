# Generated by Django 2.2.4 on 2022-02-22 18:08

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('telegram', '0020_branch_start_time'),
    ]

    operations = [
        migrations.AddField(
            model_name='branch',
            name='end_time',
            field=models.TimeField(default=django.utils.timezone.now, verbose_name='Schedule End'),
        ),
        migrations.AlterField(
            model_name='branch',
            name='start_time',
            field=models.TimeField(default=django.utils.timezone.now, verbose_name='Schedule Start'),
        ),
    ]

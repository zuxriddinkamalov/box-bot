# Generated by Django 2.2.4 on 2022-01-23 23:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0018_auto_20210707_1727'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='excel',
            options={},
        ),
        migrations.AlterField(
            model_name='photo',
            name='title',
            field=models.CharField(max_length=256, verbose_name='Title'),
        ),
    ]
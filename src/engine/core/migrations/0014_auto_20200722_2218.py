# Generated by Django 2.2.4 on 2020-07-22 17:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0013_branchbase_region'),
    ]

    operations = [
        migrations.AlterField(
            model_name='branchbase',
            name='description',
            field=models.CharField(default='', max_length=255, verbose_name='Description'),
        ),
    ]

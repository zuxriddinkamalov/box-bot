# Generated by Django 2.2.4 on 2020-07-12 11:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_config'),
    ]

    operations = [
        migrations.AddField(
            model_name='language',
            name='text',
            field=models.CharField(default="", max_length=255, verbose_name='Text'),
            preserve_default=False,
        ),
    ]

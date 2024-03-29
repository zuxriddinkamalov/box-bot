# Generated by Django 2.2.4 on 2020-07-12 11:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0006_language_text'),
    ]

    operations = [
        migrations.AddField(
            model_name='language',
            name='order',
            field=models.IntegerField(default=0, verbose_name='Language Number'),
        ),
        migrations.AlterField(
            model_name='language',
            name='text',
            field=models.CharField(default='', max_length=255, verbose_name='Text'),
        ),
    ]

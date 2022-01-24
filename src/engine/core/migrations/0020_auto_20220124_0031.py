# Generated by Django 2.2.4 on 2022-01-24 00:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0019_auto_20220123_2345'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='barcode',
            field=models.CharField(blank=True, default='', max_length=255, null=True, verbose_name='Barcode'),
        ),
        migrations.AddField(
            model_name='product',
            name='sku',
            field=models.CharField(blank=True, default='', max_length=255, null=True, verbose_name='SKU'),
        ),
    ]

# Generated by Django 2.2.4 on 2020-07-20 11:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0010_cartbase_canceled'),
    ]

    operations = [
        migrations.CreateModel(
            name='OrderStatus',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=10, verbose_name='Title')),
                ('order', models.IntegerField(default=0, verbose_name='Status Number')),
            ],
        ),
        migrations.CreateModel(
            name='OrderBase',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('delivery', models.BooleanField(default=False, verbose_name='Delivery')),
                ('time', models.CharField(default='Ближайшее время', max_length=1024, verbose_name='Time')),
                ('card', models.BooleanField(default=False, verbose_name='Card')),
                ('phone', models.BigIntegerField(default=0, verbose_name='Phone')),
                ('name', models.CharField(default='', max_length=1024, verbose_name='Name')),
                ('active', models.BooleanField(default=True, verbose_name='Active')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created at')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Last view')),
                ('status', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.OrderStatus')),
            ],
        ),
    ]
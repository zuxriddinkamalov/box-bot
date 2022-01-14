# Generated by Django 2.2.4 on 2021-07-07 12:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0017_auto_20200723_1130'),
    ]

    operations = [
        migrations.CreateModel(
            name='Excel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.FileField(upload_to='client/excels/')),
            ],
            options={
                'verbose_name': 'Загрузка списка поставщиков',
            },
        ),
        migrations.AlterField(
            model_name='branchtitle',
            name='title',
            field=models.CharField(max_length=255, verbose_name='Title'),
        ),
    ]
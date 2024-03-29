# Generated by Django 2.2.4 on 2020-07-20 12:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0013_branchbase_region'),
        ('telegram', '0013_auto_20200720_1638'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='settings',
            name='managers',
        ),
        migrations.CreateModel(
            name='Branch',
            fields=[
                ('branchbase_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='core.BranchBase')),
                ('latitude', models.FloatField(default=0.0, verbose_name='Latitude')),
                ('longitude', models.FloatField(default=0.0, verbose_name='Longitude')),
                ('managers', models.ManyToManyField(blank=True, to='telegram.User')),
            ],
            bases=('core.branchbase',),
        ),
    ]

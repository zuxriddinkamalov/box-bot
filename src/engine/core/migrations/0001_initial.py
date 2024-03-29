# Generated by Django 2.2.4 on 2020-07-11 14:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(default=None, max_length=255, verbose_name='Title')),
                ('description', models.TextField(default=None, verbose_name='Description')),
                ('active', models.BooleanField(default=False, verbose_name='Active')),
                ('order', models.IntegerField(default=0, verbose_name='Category Number')),
            ],
        ),
        migrations.CreateModel(
            name='Language',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=10, verbose_name='Title')),
            ],
        ),
        migrations.CreateModel(
            name='Photo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=10, verbose_name='Title')),
                ('file_id', models.CharField(blank=True, default=None, max_length=1024, null=True, verbose_name='Telegram File ID')),
                ('photo', models.ImageField(upload_to='media/property', verbose_name='Photo')),
            ],
        ),
        migrations.CreateModel(
            name='Settings',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=10, verbose_name='Title')),
                ('active', models.BooleanField(default=True, verbose_name='Active')),
                ('token', models.CharField(max_length=1024, verbose_name='Token')),
                ('chatbase_token', models.CharField(blank=True, max_length=1024, null=True, verbose_name='Chatbase Token')),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(default=None, max_length=255, verbose_name='Title')),
                ('description', models.TextField(default=None, verbose_name='Description')),
                ('price', models.IntegerField(default=0, verbose_name='Price')),
                ('active', models.BooleanField(default=False, verbose_name='Active')),
                ('order', models.IntegerField(default=0, verbose_name='Product Number')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.Category')),
                ('language', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='product_language', to='core.Language')),
                ('photo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.Photo')),
            ],
        ),
        migrations.CreateModel(
            name='Position',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('count', models.IntegerField(default=1, verbose_name='Product count')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.Product')),
            ],
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.IntegerField(default=0, verbose_name='Message Number')),
                ('title', models.CharField(default=None, max_length=255, verbose_name='Title')),
                ('text', models.TextField(default=None, verbose_name='Text')),
                ('language', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='message_language', to='core.Language')),
            ],
        ),
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(default=None, max_length=255, verbose_name='Title')),
                ('text', models.TextField(blank=True, null=True, verbose_name='Event text')),
                ('views', models.PositiveIntegerField(blank=True, default=0, null=True, verbose_name='Views')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created at')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Last view')),
                ('active', models.BooleanField(default=False, verbose_name='Active')),
                ('visible', models.BooleanField(default=False, verbose_name='Visible')),
                ('language', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='event_language', to='core.Language')),
                ('photo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.Photo')),
            ],
        ),
        migrations.AddField(
            model_name='category',
            name='language',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='category_language', to='core.Language'),
        ),
        migrations.AddField(
            model_name='category',
            name='photo',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.Photo'),
        ),
        migrations.CreateModel(
            name='Button',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order', models.IntegerField(default=0, verbose_name='Button Number')),
                ('button_code', models.CharField(default=None, max_length=512, verbose_name='Button unique code')),
                ('title', models.CharField(default=None, max_length=255, verbose_name='Title')),
                ('checkpoint', models.IntegerField(default=1, verbose_name='Button checkpoint group')),
                ('language', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='button_language', to='core.Language')),
            ],
        ),
        migrations.CreateModel(
            name='Announcement',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(default=None, max_length=255, verbose_name='Title')),
                ('text', models.TextField(blank=True, null=True, verbose_name='Announcement text')),
                ('views', models.PositiveIntegerField(blank=True, default=0, null=True, verbose_name='Views')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created at')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Last view')),
                ('active', models.BooleanField(default=False, verbose_name='Active')),
                ('visible', models.BooleanField(default=False, verbose_name='Visible')),
                ('language', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='news_language', to='core.Language')),
                ('photo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.Photo')),
            ],
        ),
    ]

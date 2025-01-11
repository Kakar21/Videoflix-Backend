# Generated by Django 5.1.4 on 2025-01-11 18:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('videos', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='video',
            name='category',
            field=models.CharField(choices=[('documentary', 'Documentary'), ('drama', 'Drama'), ('romance', 'Romance')], default='new', max_length=16),
        ),
        migrations.AddField(
            model_name='video',
            name='new',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='video',
            name='thumbnail',
            field=models.ImageField(null=True, upload_to='thumbnails'),
        ),
        migrations.AlterField(
            model_name='video',
            name='description',
            field=models.TextField(max_length=500),
        ),
        migrations.AlterField(
            model_name='video',
            name='title',
            field=models.CharField(max_length=100),
        ),
    ]

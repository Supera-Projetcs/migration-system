# Generated by Django 5.0.8 on 2024-08-11 17:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('processes', '0003_uploadedfile_remove_processchunk_process_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='uploadedfile',
            name='error_count',
            field=models.IntegerField(blank=True, default=0),
        ),
        migrations.AlterField(
            model_name='uploadedfile',
            name='success_count',
            field=models.IntegerField(blank=True, default=0),
        ),
    ]

# Generated by Django 5.0.8 on 2024-08-09 18:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('processes', '0004_alter_genomescore_movieid_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='movie',
            old_name='id',
            new_name='movieId',
        ),
    ]

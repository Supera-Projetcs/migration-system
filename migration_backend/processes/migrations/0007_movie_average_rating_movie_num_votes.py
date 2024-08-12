# Generated by Django 5.0.8 on 2024-08-12 16:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('processes', '0006_alter_rating_movieid_alter_tag_movieid'),
    ]

    operations = [
        migrations.AddField(
            model_name='movie',
            name='average_rating',
            field=models.FloatField(default=0, null=True),
        ),
        migrations.AddField(
            model_name='movie',
            name='num_votes',
            field=models.IntegerField(default=0, null=True),
        ),
    ]

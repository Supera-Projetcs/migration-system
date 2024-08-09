# Generated by Django 5.0.8 on 2024-08-08 16:38

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Rating',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rating', models.IntegerField()),
                ('user', models.IntegerField()),
                ('movie', models.IntegerField()),
                ('timestamp', models.CharField(max_length=100)),
            ],
            options={
                'db_table': 'ratings',
            },
        ),
    ]

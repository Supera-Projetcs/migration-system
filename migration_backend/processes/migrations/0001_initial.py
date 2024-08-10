# Generated by Django 5.0.8 on 2024-08-10 18:25

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='GenomeScore',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('movieid', models.IntegerField(db_column='movieid')),
                ('tagid', models.IntegerField(null=True)),
                ('relevance', models.FloatField(null=True)),
            ],
            options={
                'db_table': 'genome_scores',
            },
        ),
        migrations.CreateModel(
            name='GenomeTag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tagid', models.IntegerField(null=True)),
                ('tag', models.CharField(max_length=255, null=True)),
            ],
            options={
                'db_table': 'genome_tags',
            },
        ),
        migrations.CreateModel(
            name='Link',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('movieid', models.IntegerField(db_column='movieid')),
                ('imdbid', models.CharField(max_length=100, null=True)),
                ('tmdbid', models.CharField(max_length=100, null=True)),
            ],
            options={
                'db_table': 'links',
            },
        ),
        migrations.CreateModel(
            name='Movie',
            fields=[
                ('movieid', models.IntegerField(primary_key=True, serialize=False, unique=True)),
                ('title', models.CharField(max_length=255, null=True)),
                ('genres', models.CharField(max_length=255, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Process',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('started', models.DateTimeField(auto_now_add=True)),
                ('number_of_chunks', models.IntegerField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Rating',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('userid', models.IntegerField(null=True)),
                ('movieid', models.IntegerField(null=True)),
                ('rating', models.FloatField(null=True)),
                ('timestamp', models.CharField(max_length=100, null=True)),
            ],
            options={
                'db_table': 'ratings',
            },
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('userid', models.IntegerField(null=True)),
                ('movieid', models.IntegerField(null=True)),
                ('tag', models.CharField(max_length=255, null=True)),
                ('timestamp', models.CharField(max_length=100, null=True)),
            ],
            options={
                'db_table': 'tags',
            },
        ),
        migrations.CreateModel(
            name='ProcessChunk',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ended', models.DateTimeField(auto_now_add=True)),
                ('start_row', models.IntegerField(null=True)),
                ('end_row', models.IntegerField(null=True)),
                ('status', models.CharField(max_length=255, null=True)),
                ('errors', models.TextField(null=True)),
                ('process', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='processes.process')),
            ],
        ),
    ]

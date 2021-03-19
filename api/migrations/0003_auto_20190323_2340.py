# Generated by Django 2.1.5 on 2019-03-23 23:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_movies_movie_genre'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='movies',
            name='movie_genre',
        ),
        migrations.AddField(
            model_name='movies',
            name='movie_genre',
            field=models.ManyToManyField(to='api.MovieService'),
        ),
    ]
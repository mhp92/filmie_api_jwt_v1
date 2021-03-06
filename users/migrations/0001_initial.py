# Generated by Django 2.1.5 on 2019-02-27 17:03

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Users',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=255, unique=True)),
                ('email', models.CharField(max_length=255, unique=True)),
                ('password', models.CharField(max_length=255)),
                ('gender', models.CharField(blank=True, max_length=255, null=True)),
                ('avatar', models.CharField(blank=True, max_length=255, null=True)),
                ('remember_token', models.CharField(blank=True, max_length=100, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('is_admin', models.BooleanField(default=False)),
                ('last_login', models.DateTimeField(auto_now_add=True)),
                ('year_of_birth', models.IntegerField(blank=True, null=True)),
                ('language', models.CharField(blank=True, max_length=32, null=True)),
                ('verified', models.BooleanField(default=True)),
            ],
            options={
                'db_table': 'users',
                'managed': False,
            },
        ),
    ]

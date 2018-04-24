# Generated by Django 2.0.2 on 2018-04-23 03:22

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='BetInfo',
            fields=[
                ('bet_id', models.AutoField(primary_key=True, serialize=False)),
                ('option', models.CharField(default='Null', max_length=20)),
                ('total_amount', models.IntegerField(default=0)),
                ('total_users', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='BetOnAdmins',
            fields=[
                ('admin_identity', models.CharField(max_length=40, primary_key=True, serialize=False)),
                ('secret_key', models.CharField(max_length=20)),
                ('login_time', models.DateTimeField(null=True, verbose_name='login')),
                ('last_active_time', models.DateTimeField(null=True, verbose_name='lastactive')),
                ('password', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Bets',
            fields=[
                ('bet_id', models.AutoField(primary_key=True, serialize=False)),
                ('option', models.CharField(default='Null', max_length=20)),
                ('amount', models.IntegerField(default=0)),
                ('date_of_placing_bet', models.DateField(default=datetime.date.today, verbose_name='Date')),
            ],
        ),
        migrations.CreateModel(
            name='Topics',
            fields=[
                ('topic_id', models.AutoField(primary_key=True, serialize=False)),
                ('topic_name', models.CharField(max_length=100)),
                ('start_date', models.DateField(verbose_name='Date')),
                ('end_date', models.DateField(verbose_name='Date')),
                ('date_of_creation', models.DateField(default=datetime.date.today, verbose_name='Date')),
                ('winning_option', models.CharField(default='not declared', max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Userinfo',
            fields=[
                ('username', models.CharField(max_length=20, primary_key=True, serialize=False)),
                ('password', models.CharField(max_length=20)),
                ('emailID', models.CharField(max_length=30)),
                ('balance', models.IntegerField(default=0)),
            ],
        ),
        migrations.AddField(
            model_name='topics',
            name='creator_name',
            field=models.ForeignKey(on_delete=models.SET(0), to='beton.Userinfo'),
        ),
        migrations.AddField(
            model_name='bets',
            name='topic_id',
            field=models.ForeignKey(on_delete=models.SET(0), to='beton.Topics'),
        ),
        migrations.AddField(
            model_name='bets',
            name='username',
            field=models.ForeignKey(on_delete=models.SET(0), to='beton.Userinfo'),
        ),
        migrations.AddField(
            model_name='betinfo',
            name='topic_id',
            field=models.ForeignKey(on_delete=models.SET(0), to='beton.Topics'),
        ),
    ]

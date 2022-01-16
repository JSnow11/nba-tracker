# Generated by Django 2.2.5 on 2022-01-16 18:18

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0011_update_proxy_permissions'),
    ]

    operations = [
        migrations.CreateModel(
            name='Conference',
            fields=[
                ('name', models.CharField(max_length=100, primary_key=True, serialize=False, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Division',
            fields=[
                ('name', models.CharField(max_length=100, primary_key=True, serialize=False, unique=True)),
                ('conference', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tracker.Conference')),
            ],
        ),
        migrations.CreateModel(
            name='Player',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
                ('country', models.CharField(max_length=100)),
                ('img_url', models.CharField(max_length=100)),
                ('position', models.CharField(max_length=4)),
                ('number', models.CharField(max_length=2)),
                ('min_per_game', models.FloatField()),
                ('pts_per_game', models.FloatField()),
                ('field_goal', models.FloatField()),
                ('three_p_ptg', models.FloatField()),
                ('ft_ptg', models.FloatField()),
                ('reb_per_game', models.FloatField()),
                ('ast_per_game', models.FloatField()),
                ('tov_per_game', models.FloatField()),
                ('stl_per_game', models.FloatField()),
                ('blk_per_game', models.FloatField()),
                ('plus_minus', models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name='PlayerSearchCounter',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('count', models.IntegerField(default=0)),
                ('player', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='tracker.Player')),
            ],
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('fav_player', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='tracker.Player')),
            ],
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('name', models.CharField(max_length=100, primary_key=True, serialize=False, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Team',
            fields=[
                ('name', models.CharField(max_length=100, unique=True)),
                ('logo_url', models.CharField(max_length=100, unique=True)),
                ('abbreviation', models.CharField(max_length=3, primary_key=True, serialize=False, unique=True)),
                ('wins', models.IntegerField()),
                ('losses', models.IntegerField()),
                ('conference', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tracker.Conference')),
                ('division', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tracker.Division')),
            ],
        ),
        migrations.CreateModel(
            name='TeamSearchCounter',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('count', models.IntegerField(default=0)),
                ('profile', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tracker.Profile')),
                ('team', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='tracker.Team')),
            ],
        ),
        migrations.AddField(
            model_name='profile',
            name='fav_team',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='tracker.Team'),
        ),
        migrations.AddField(
            model_name='profile',
            name='searched_players',
            field=models.ManyToManyField(related_name='searched_players', through='tracker.PlayerSearchCounter', to='tracker.Player'),
        ),
        migrations.AddField(
            model_name='profile',
            name='searched_teams',
            field=models.ManyToManyField(related_name='searched_teams', through='tracker.TeamSearchCounter', to='tracker.Team'),
        ),
        migrations.AddField(
            model_name='playersearchcounter',
            name='profile',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tracker.Profile'),
        ),
        migrations.AddField(
            model_name='player',
            name='tags',
            field=models.ManyToManyField(to='tracker.Tag'),
        ),
        migrations.AddField(
            model_name='player',
            name='team',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tracker.Team'),
        ),
        migrations.CreateModel(
            name='Match',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('local_pts', models.IntegerField()),
                ('visitor_pts', models.IntegerField()),
                ('local', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='local', to='tracker.Team')),
                ('visitor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='visitor', to='tracker.Team')),
            ],
        ),
    ]

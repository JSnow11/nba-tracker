# Generated by Django 2.2.5 on 2022-01-15 11:54

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0011_update_proxy_permissions'),
        ('tracker', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='PlayerSearchCounter',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('count', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AlterField(
            model_name='match',
            name='id',
            field=models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='player',
            name='id',
            field=models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
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
            name='fav_player',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='tracker.Player'),
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
            name='player',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='tracker.Player'),
        ),
        migrations.AddField(
            model_name='playersearchcounter',
            name='profile',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tracker.Profile'),
        ),
    ]

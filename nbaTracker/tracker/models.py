from enum import unique
from django.db import models

# Create your models here.


class Conference(models.Model):
    name = models.CharField(max_length=100, unique=True, primary_key=True)


class Division(models.Model):
    name = models.CharField(max_length=100, unique=True, primary_key=True)

    conference = models.ForeignKey(Conference, on_delete=models.CASCADE)


class Team(models.Model):
    name = models.CharField(max_length=100, unique=True)
    logo_url = models.CharField(max_length=100, unique=True)
    abbreviation = models.CharField(
        max_length=3, unique=True, primary_key=True)

    wins = models.IntegerField()
    losses = models.IntegerField()

    division = models.ForeignKey(Division, on_delete=models.CASCADE)
    conference = models.ForeignKey(Conference, on_delete=models.CASCADE)


class Match(models.Model):
    local_pts = models.IntegerField()
    visitor_pts = models.IntegerField()

    local = models.ForeignKey(
        Team, on_delete=models.CASCADE, related_name='local')
    visitor = models.ForeignKey(
        Team, on_delete=models.CASCADE, related_name='visitor')


class Tag(models.Model):
    name = models.CharField(max_length=100, unique=True, primary_key=True)


class Player(models.Model):
    name = models.CharField(max_length=100, unique=True)

    img_url = models.CharField(max_length=100)
    position = models.CharField(max_length=4)
    number = models.CharField(max_length=2)

    min_per_game = models.FloatField()
    pts_per_game = models.FloatField()
    field_goal = models.FloatField()
    three_p_ptg = models.FloatField()
    ft_ptg = models.FloatField()
    reb_per_game = models.FloatField()
    ast_per_game = models.FloatField()
    tov_per_game = models.FloatField()
    stl_per_game = models.FloatField()
    blk_per_game = models.FloatField()

    plus_minus = models.FloatField()

    tags = models.ManyToManyField(Tag)
    team = models.ForeignKey('Team', on_delete=models.CASCADE)


class Profile(models.Model):
    user = models.OneToOneField(
        'auth.User', on_delete=models.CASCADE, primary_key=True)

    fav_team = models.ForeignKey(Team, on_delete=models.SET_NULL, null=True)
    fav_player = models.ForeignKey(
        Player, on_delete=models.SET_NULL, null=True)

    searched_players = models.ManyToManyField(
        Player, related_name='searched_players', through="PlayerSearchCounter")
    searched_teams = models.ManyToManyField(
        Team, related_name='searched_teams', through="TeamSearchCounter")


class TeamSearchCounter(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    team = models.ForeignKey(Team, on_delete=models.CASCADE, null=True)

    count = models.IntegerField(default=0)


class PlayerSearchCounter(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    player = models.ForeignKey(Player, on_delete=models.CASCADE, null=True)

    count = models.IntegerField(default=0)

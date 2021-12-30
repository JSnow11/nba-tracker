from django.db import models

# Create your models here.


class Conference(models.Model):
    name = models.CharField(max_length=100, unique=True)


class Division(models.Model):
    name = models.CharField(max_length=100)

    conference = models.ForeignKey(Conference, on_delete=models.CASCADE)


class Team(models.Model):
    name = models.CharField(max_length=100, unique=True)
    img_url = models.CharField(max_length=100)
    wins = models.IntegerField()
    losses = models.IntegerField()

    win_percentage = wins / (wins + losses)

    division = models.ForeignKey(Division, on_delete=models.CASCADE)
    conference = models.ForeignKey(Conference, on_delete=models.CASCADE)


class Match(models.Model):
    local_pts = models.IntegerField()
    visitor_pts = models.IntegerField()

    local = models.ForeignKey(
        Team, on_delete=models.CASCADE, related_name='local')
    visitor = models.ForeignKey(
        Team, on_delete=models.CASCADE, related_name='visitor')


class Player(models.Model):
    name = models.CharField(max_length=100)
    img_url = models.CharField(max_length=100)
    position = models.CharField(max_length=4)
    number = models.CharField(max_length=2)

    min_per_game = models.FloatField()
    pts_per_game = models.FloatField()
    field_goal = models.FloatField(min=0, max=100)
    reb_per_game = models.FloatField()
    ast_per_game = models.FloatField()
    rob_per_game = models.FloatField()
    blk_per_game = models.FloatField()

    team = models.ForeignKey('Team', on_delete=models.CASCADE)

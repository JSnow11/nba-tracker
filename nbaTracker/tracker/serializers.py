from django.contrib.auth.models import User, Group
from rest_framework import serializers

from .models import Team, Player


class TeamSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Team
        fields = ['name', 'logo_url', 'wins', 'losses',
                  'win_percentage', 'division', 'conference']


class PlayerSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Player
        fields = ['name', 'img_url', 'position', 'number',
                  'min_per_game', 'pts_per_game', 'field_goal',
                  'reb_per_game', 'ast_per_game', 'rob_per_game',
                  'blk_per_game', 'team']

from django.contrib.auth.models import User, Group
from rest_framework import serializers

from .models import Team, Player


class TeamSerializer(serializers.HyperlinkedModelSerializer):
    division = serializers.SerializerMethodField()
    conference = serializers.SerializerMethodField()

    class Meta:
        model = Team
        fields = ['name', 'logo_url', 'wins', 'losses',
                  'division', 'conference']

    def get_division(self, obj):
        return obj.division.name

    def get_conference(self, obj):
        return obj.conference.name


class PlayerSerializer(serializers.HyperlinkedModelSerializer):
    team = serializers.SerializerMethodField()

    class Meta:
        model = Player
        fields = ['name', 'min_per_game', 'pts_per_game', 'field_goal',
                  'three_p_ptg', 'ft_ptg', 'reb_per_game',
                  'ast_per_game', 'tov_per_game', 'stl_per_game',
                  'blk_per_game', 'team']

    def get_team(self, obj):
        return TeamSerializer(obj.team).data

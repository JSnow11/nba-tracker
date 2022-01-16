from django.contrib.auth.models import User, Group
from rest_framework import serializers

from .models import Tag, Team, Player


class TeamSerializer(serializers.HyperlinkedModelSerializer):
    division = serializers.SerializerMethodField()
    conference = serializers.SerializerMethodField()

    class Meta:
        model = Team
        fields = ['name', 'logo_url', 'wins', 'losses',
                  'division', 'conference', 'abbreviation']

    def get_division(self, obj):
        return obj.division.name

    def get_conference(self, obj):
        return obj.conference.name


class TeamWithRoasterSerializer(serializers.HyperlinkedModelSerializer):
    division = serializers.SerializerMethodField()
    conference = serializers.SerializerMethodField()
    players = serializers.SerializerMethodField()

    class Meta:
        model = Team
        fields = ['name', 'logo_url', 'wins', 'losses',
                  'division', 'conference', "players"]

    def get_division(self, obj):
        return obj.division.name

    def get_conference(self, obj):
        return obj.conference.name

    def get_players(self, obj):
        return PlayerWithoutTeamSerializer(Player.objects.filter(team=obj), many=True, context=self.context).data


class PlayerWithoutTeamSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Player
        fields = ['name', 'min_per_game', 'pts_per_game', 'field_goal',
                  'three_p_ptg', 'ft_ptg', 'reb_per_game',
                  'ast_per_game', 'tov_per_game', 'stl_per_game',
                  'blk_per_game']


class TagSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Tag
        fields = ['name']


class PlayerSerializer(serializers.HyperlinkedModelSerializer):
    team = serializers.SerializerMethodField()
    tags = serializers.SerializerMethodField()

    class Meta:
        model = Player
        fields = ['name', 'number', 'position', 'img_url', 'min_per_game', 'pts_per_game', 'field_goal',
                  'three_p_ptg', 'ft_ptg', 'reb_per_game',
                  'ast_per_game', 'tov_per_game', 'stl_per_game',
                  'blk_per_game', 'team', 'plus_minus', 'tags']

    def get_team(self, obj):
        return TeamSerializer(obj.team).data

    def get_tags(self, obj):
        return TagSerializer(obj.tags, many=True, context=self.context).data

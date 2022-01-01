from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework import permissions
from rest_framework.views import APIView

from tracker.models import Profile, Team, Player
from tracker.serializers import TeamSerializer, PlayerSerializer

from tracker.populate import populate_database
from tracker.search import index_items, search_players, search_teams
from tracker.recommendations import recommend_players_by_stats, recommend_players_by_tags


# Create your views here.


class Log(APIView):
    """
    View to log in/out a user
    """

    def post(self, request):
        user = authenticate(request=request, username=request.data.get(
            "username"), password=request.data.get("password"))

        if not user:
            return Response({"error": "Invalid credentials"}, status=401)

        request.session["user_id"] = user.id

        return Response({"token": user.auth_token.key})

    def delete(self, request):
        request.session["user_id"] = None

        return Response({})


class Register(APIView):
    """
    View to register a user
    """

    def post(self, request):
        user = User(username=request.data.get("username"), email=request.data.get(
            "email"), password=request.data.get("password"))
        user.save()

        if not user:
            return Response({"error": "Invalid user"}, status=401)

        profile = Profile(user=user, fav_team=request.data.get(
            "fav_team"), fav_player=request.data.get("fav_player"))
        profile.save()

        if not profile:
            user.delete()
            return Response({"error": "Invalid profile data"}, status=401)

        user = authenticate(request=request, username=request.data.get(
            "username"), password=request.data.get("password"))

        if not user:
            return Response({"error": "Couldn't authenticate"}, status=401)

        return Response({"token": user.auth_token.key})


class PopulateDB(APIView):
    """
    View to populate the app db
    """
    permission_classes = [permissions.IsAdminUser]

    def get(self, request, format=None):
        """
        Triggers scrapping and population
        """
        [n_of_teams, n_of_players] = populate_database()
        return Response({"n_of_teams": n_of_teams, "n_of_players": n_of_players})


class IndexItems(APIView):
    """
    View to index items for search
    """
    permission_classes = [permissions.IsAdminUser]

    def get(self, request, format=None):
        """
        Triggers items indexing
        """
        indexed_teams, indexed_players = index_items()
        return Response({"indexed_teams": indexed_teams, "indexed_players": indexed_players})


class SearchTeams(APIView):
    """
    View to search teams
    """

    def get(self, request, format=None):
        """
        Search teams
        """
        query = request.query_params.get('query', None)
        if query is None:
            return Response({"error": "Query parameter is required"}, status=400)

        if query == "":
            teams = Team.objects.all()
        else:
            teams = search_teams(query)

        if('user_id' in request.session and len(teams) == 1):
            user = Profile.objects.get(id=request.session['user_id'])
            user.searched_players.add(teams[0])
            user.save()

        serializer = TeamSerializer(
            teams, many=True, context={"request": request})

        return Response(serializer.data)


class SearchPlayers(APIView):
    """
    View to search players
    """

    def get(self, request, format=None):
        """
        Search players
        """
        query = request.query_params.get('query', None)
        if query is None:
            return Response({"error": "Query parameter is required"}, status=400)

        if query == "":
            players = Player.objects.all()
        else:
            players = search_players(query)

        if('user_id' in request.session and len(players) == 1):
            user = Profile.objects.get(id=request.session['user_id'])
            user.searched_players.add(players[0])
            user.save()

        serializer = PlayerSerializer(
            players, many=True, context={"request": request})
        return Response(serializer.data)


class RecommendPlayers(APIView):
    """
    View to recommend players
    """

    def get(self, request, format=None):
        """
        Recommend players
        """
        profile = Profile.objects.get(id=request.session['user_id'])

        players_by_stats = recommend_players_by_stats(profile)
        players_by_tags = recommend_players_by_tags(profile)

        stat_serializer = PlayerSerializer(
            players_by_stats, many=True, context={"request": request})
        tag_serializer = PlayerSerializer(
            players_by_tags, many=True, context={"request": request})

        return Response({"by_stat": stat_serializer.data, "by_tags": tag_serializer.data})


class TeamViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows teams to be viewed or edited.
    """
    queryset = Team.objects.all().order_by('-name')
    serializer_class = TeamSerializer
    permission_classes = [permissions.IsAuthenticated]


class PlayerViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows players to be viewed or edited.
    """
    queryset = Player.objects.all().order_by('-name')
    serializer_class = PlayerSerializer
    permission_classes = [permissions.IsAuthenticated]

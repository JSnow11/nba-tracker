from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework import permissions
from rest_framework.views import APIView

from tracker.models import Profile, Team, Player
from tracker.serializers import TeamSerializer, PlayerSerializer, TeamWithRoasterSerializer

from tracker.populate import populate_database
from tracker.search import index_items, search_players, search_teams
from tracker.recommendations import recommend_players_by_stats, recommend_players_by_tags, recommend_teams_by_search


# Create your views here.


class Log(APIView):
    """
    View to log in/out a user
    """
    serializer_class = AuthTokenSerializer

    def post(self, request):
        user_serializer = self.serializer_class(data=request.data,
                                                context={'request': request})

        user_serializer.is_valid(raise_exception=True)
        user = user_serializer.validated_data['user']

        token, created = Token.objects.get_or_create(user=user)
        token.save()

        response = Response({})
        response.set_cookie('token', token.key)
        token.user.is_superuser and response.set_cookie('admin', 'true')

        return response

    def delete(self, request):
        request.session["user_id"] = None

        response = Response({})
        response.delete_cookie('token')
        response.delete_cookie('admin')

        return response


class Register(APIView):
    """
    View to register a user
    """

    def post(self, request):
        user = User(username=request.data.get("username"), email=request.data.get(
            "email"), password=request.data.get("password"))
        user.set_password(user.password)
        user.save()

        if not user:
            return Response({"error": "Invalid user"}, status=401)

        profile = Profile(user=user)
        profile.save()

        if not profile:
            user.delete()
            return Response({"error": "Invalid profile data"}, status=401)

        return Response({})


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

        if(request.user and request.user.id and len(teams) == 1):
            print("ID OF THE USER: " + str(request.user.id))
            profile = Profile.objects.get(user_id=request.user.id)

            profile.searched_teams.add(teams[0])
            profile.save()

            counter = profile.teamsearchcounter_set.filter(
                team_id=teams[0].abbreviation)

            if counter:
                counter.update(count=counter[0].count + 1)

        serializer = (TeamWithRoasterSerializer(
            teams, many=True, context={"request": request}) if len(teams) == 1 else TeamSerializer(teams, many=True, context={"request": request}))

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

        if(request.user and request.user.id and len(players) == 1):
            print("ID OF THE USER: " + str(request.user.id))
            profile = Profile.objects.get(user_id=request.user.id)

            profile.searched_players.add(players[0])
            profile.save()

            counter = profile.playersearchcounter_set.filter(
                player_id=players[0].id)

            if counter:
                counter.update(count=counter[0].count + 1)

        serializer = PlayerSerializer(
            players, many=True, context={"request": request})
        return Response(serializer.data)


class RecommendPlayers(APIView):
    """
    View to recommend players
    """

    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, format=None):
        """
        Recommend players
        """
        try:
            profile = Profile.objects.get_or_create(user_id=request.user.id)
        except Profile.DoesNotExist:
            return Response({"error": "Profile not found, you need to register"}, status=400)

        players_by_stats = recommend_players_by_stats(profile[0])
        players_by_tags = recommend_players_by_tags(profile[0])

        stat_serializer = PlayerSerializer(
            [p["player"] for p in players_by_stats], many=True, context={"request": request})
        tag_serializer = PlayerSerializer(
            [p["player"] for p in players_by_tags], many=True, context={"request": request})

        return Response({"by_stat": stat_serializer.data, "by_tags": tag_serializer.data})


class RecommendTeams(APIView):
    """
    View to recommend teams
    """

    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, format=None):
        """
        Recommend teams
        """
        try:
            profile = Profile.objects.get(user_id=request.user.id)
        except Profile.DoesNotExist:
            return Response({"error": "Profile not found, you need to register"}, status=400)

        teams_by_search = recommend_teams_by_search(profile)

        search_serializer = TeamSerializer(
            teams_by_search, many=True, context={"request": request})

        return Response({"by_search": search_serializer.data})


class StatLeaders(APIView):
    """
    View to get stat leaders
    """

    def get(self, request, format=None):
        """
        Get stat leaders
        """

        players = Player.objects.all()

        ppg_leader = PlayerSerializer(
            players.order_by('-pts_per_game')[0]).data
        apg_leader = PlayerSerializer(
            players.order_by('-ast_per_game')[0]).data
        rpg_leader = PlayerSerializer(
            players.order_by('-reb_per_game')[0]).data
        blk_leader = PlayerSerializer(
            players.order_by('-blk_per_game')[0]).data

        return Response({"ppg": ppg_leader, "apg": apg_leader, "rpg": rpg_leader, "blk": blk_leader})


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

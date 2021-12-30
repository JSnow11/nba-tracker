from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework import permissions
from rest_framework.views import APIView

from tracker.models import Team, Player
from tracker.serializers import TeamSerializer, PlayerSerializer

from .populate import populate_database

# Create your views here.


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

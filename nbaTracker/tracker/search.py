import os
import shutil

from .models import Team, Player

from whoosh import query
from whoosh.fields import Schema, TEXT
from whoosh.index import create_in, open_dir
from whoosh.qparser import QueryParser

from whoosh.qparser.default import MultifieldParser

index = "tracker/search_index"


def index_items():
    if os.path.exists(index):
        shutil.rmtree(index)
    os.mkdir(index)

    os.mkdir(os.path.join(index, "teams"))
    indexed_teams = index_teams()

    os.mkdir(os.path.join(index, "players"))
    indexed_players = index_players()

    return indexed_teams, indexed_players


def get_player_schema():
    return Schema(
        name=TEXT(stored=True),

        team_abbr=TEXT(stored=True),
        team=TEXT(stored=True),
        tags=TEXT(stored=True),
        country=TEXT(stored=True),
        pos=TEXT(stored=True),
        number=TEXT(stored=True),
    )


def get_team_schema():
    return Schema(
        name=TEXT(stored=True),
        abbreviation=TEXT(stored=True),
        division=TEXT(stored=True),
        conference=TEXT(stored=True),
    )


def index_teams():
    teams = Team.objects.all()

    ix = create_in(index + "/teams", schema=get_team_schema())
    writer = ix.writer()

    for team in teams:
        writer.add_document(name=team.name,
                            abbreviation=team.abbreviation,
                            division=team.division.name,
                            conference=team.division.conference.name)

    writer.commit()
    print("{} teams indexed".format(ix.doc_count()))
    return ix.doc_count()


def index_players():
    players = Player.objects.all()

    ix = create_in(index + "/players", schema=get_player_schema())
    writer = ix.writer()

    for player in players:
        writer.add_document(name=player.name, team_abbr=player.team.abbreviation,
                            team=player.team.name, tags="".join(
                                [t.name for t in player.tags.all()]),
                            number=str(player.number), country=player.country, pos=player.position)
    writer.commit()
    print("{} players indexed".format(ix.doc_count()))
    return ix.doc_count()


def search_teams(keywords):
    ix = open_dir(index + "/teams")
    with ix.searcher() as searcher:
        print("Searching for teams, keywords: {}".format(keywords))
        query = MultifieldParser(
            ["name", "abbreviation", "division", "conference"], ix.schema).parse(str(keywords))
        results = searcher.search(query, limit=None)
        if(len(results) > 0):
            team_abbreviations = [r["abbreviation"] for r in results]
            return Team.objects.filter(abbreviation__in=team_abbreviations)
        else:
            return []


def search_players(keywords):
    ix = open_dir(index + "/players")
    with ix.searcher() as searcher:
        print("Searching for players, keywords: {}".format(keywords))
        query = MultifieldParser(
            ["name", "team_abbr", "team", "tags", "country", "pos", "number"], ix.schema).parse(str(keywords))
        results = searcher.search(query, limit=None)
        if(len(results) > 0):
            player_names = [r["name"] for r in results]
            return Player.objects.filter(name__in=player_names)
        else:
            return []

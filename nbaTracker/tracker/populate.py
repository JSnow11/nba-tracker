from tracker.scrapping import scrap_players, scrap_teams
from tracker.models import Conference, Division, Team, Match, Player

path = "hetrec2011-lastfm-2k"


def populate_database():
    print('Populating database...')

    print('Deleting tables...')
    delete_tables()

    print('Scrapping conferences, divisions and teams...')
    teams, conferences, divisions = scrap_teams()

    print("Populating conferences, divisions and teams...")
    populate_conferences(conferences)
    populate_divisions(divisions)
    populate_teams(teams)

    print('Scrapping players...')
    players = scrap_players()
    print("Populating players...")
    populate_players(players)

    print('Populating matches...')
    # todo: matches = scrap_matches()
    print('Finished database population')
    return [len(teams), len(players)]


def delete_tables():
    Conference.objects.all().delete()
    Division.objects.all().delete()
    Team.objects.all().delete()
    Match.objects.all().delete()


def populate_conferences(conferences):
    print(conferences)
    for c in conferences:
        Conference.objects.create(name=c)

    print("Conferences inserted: {}".format(len(conferences)))


def populate_divisions(divisions):
    print(divisions)
    for d in divisions:
        conf = Conference.objects.get(name=d["conference"])
        Division.objects.create(name=d["division"], conference=conf)


def populate_teams(teams):
    create_queue = []
    for t in teams:
        conf = Conference.objects.get(name=t["conference"])
        div = Division.objects.get(name=t["division"], conference=conf)

        create_queue.append(Team(
            name=t["name"],
            abbreviation=t["abbreviation"],
            conference=conf,
            division=div,
            logo_url=t["img_url"],
            wins=t["wins"],
            losses=t["losses"],
        ))
    Team.objects.bulk_create(create_queue)
    print("Teams inserted: {}".format(len(create_queue)))


def populate_players(players):
    create_queue = []
    for p in players:
        team = Team.objects.get(abbreviation=p["team"])
        create_queue.append(Player(
            name=p["name"],
            min_per_game=p["min_per_game"],
            pts_per_game=p["pts_per_game"],
            field_goal=p["field_goal"],
            three_p_ptg=p["three_p_ptg"],
            ft_ptg=p["ft_ptg"],
            reb_per_game=p["reb_per_game"],
            ast_per_game=p["ast_per_game"],
            tov_per_game=p["tov_per_game"],
            stl_per_game=p["stl_per_game"],
            blk_per_game=p["blk_per_game"],
            plus_minus=p["plus_minus"],
            team=team
        ))
    Player.objects.bulk_create(create_queue)
    print("Players inserted: {}".format(len(create_queue)))

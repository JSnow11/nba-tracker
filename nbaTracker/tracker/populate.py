from tracker.scrapping import scrap_players, scrap_teams
from tracker.models import Conference, Division, Team, Match, Player, Tag


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

    print('Populating tags...')
    populate_tags()

    print('Scrapping players...')
    players = scrap_players()
    print("Populating players...")
    populate_players(players)

    print('Populating matches...')
    print('Finished database population')
    return [len(teams), len(players)]


def delete_tables():
    Player.objects.all().delete()
    Tag.objects.all().delete()
    Team.objects.all().delete()
    Division.objects.all().delete()
    Conference.objects.all().delete()


def populate_tags():
    for t in ["ANOTADOR", "ASISTENTE", "3PT", "DEFENSOR", "REBOTEADOR", "STAR"]:
        Tag.objects.create(name=t)


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


def add_player_tags():
    players = Player.objects.all()
    for player in players:
        if(player.pts_per_game > 20 and player.field_goal > 0.4 and player.three_p_ptg > 0.33 and player.ft_ptg > 0.75):
            player.tags.add("ANOTADOR")
        if(player.ast_per_game > 8):
            player.tags.add("ASISTENTE")
        if(player.three_p_ptg > 0.4):
            player.tags.add("3PT")
        if(player.reb_per_game > 10):
            player.tags.add("REBOTEADOR")
        if(player.stl_per_game > 3 and player.blk_per_game > 3):
            player.tags.add("DEFENSOR")
        if(player.blk_per_game > 5):
            player.tags.add("TAPONADOR")
        if(player.stl_per_game > 5):
            player.tags.add("LADRON")
        if(player.pts_per_game > 10 and player.ast_per_game > 5 and player.plus_minus > 10):
            player.tags.add("STAR")

        player.save()


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
    add_player_tags()
    print("Added player tags")

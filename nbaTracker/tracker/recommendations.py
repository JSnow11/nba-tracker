import random

from tracker.models import Player, Team


def get_player_stats(player):
    return [player.min_per_game, player.pts_per_game, player.field_goal,
            player.three_p_ptg, player.ft_ptg, player.reb_per_game,
            player.ast_per_game, player.tov_per_game, player.stl_per_game,
            player.blk_per_game]


def players_stats_mean(players, counters):
    mean = {}
    i = 0
    for player in players:
        mean["mpg"] += player.min_per_game * counters[i]
        mean["pts"] += player.pts_per_game * counters[i]
        mean["fg"] += player.field_goal * counters[i]
        mean["3p"] += player.three_p_ptg * counters[i]
        mean["ft"] += player.ft_ptg * counters[i]
        mean["reb"] += player.reb_per_game * counters[i]
        mean["ast"] += player.ast_per_game * counters[i]
        mean["tov"] += player.tov_per_game * counters[i]
        mean["stl"] += player.stl_per_game * counters[i]
        mean["blk"] += player.blk_per_game * counters[i]
        i += 1

    for key in mean:
        mean[key] /= len(players)

    return mean.values()


def compute_stats_similarities(players, search_player_mean):
    print('Computing search-player similarity matrix')
    return sorted([{"distance": manhattan_distance(get_player_stats(player), search_player_mean), "player": player} for player in players], key=lambda x: x["distance"])[:10]


def recommend_players_by_stats(profile):
    searched_players = profile.searched_players.all()
    counters = [c["count"]
                for c in profile.player_search_counter_set.all()]

    players = Player.objects.all()
    searched_players_stat_mean = players_stats_mean(searched_players, counters)

    return [p["player"] for p in compute_stats_similarities(players, searched_players_stat_mean)]


def players_frequent_tags(searched_players, counters):
    frec = {}
    i = 0
    for player in searched_players:
        for tag in player.tags.all() * counters[i]:
            if tag in frec.keys():
                frec[tag] = frec.get(tag, 0) + 1
            else:
                frec[tag] = 1

    return [k for k, v in sorted(frec.items(), key=lambda item: item[1], reverse=True)]


def compute_tags_similarities(players, search_frequent_tags):
    print('Computing tags-player similarity matrix')
    return sorted([{"value": dice_coefficient(player.tags.all(), search_frequent_tags), "player": player} for player in players], key=lambda x: x["value"])[:10]


def recommend_players_by_tags(profile):
    searched_players = profile.searched_players.all()
    counters = [c["count"]
                for c in profile.player_search_counter_set.all()]

    players = Player.objects.all()
    searched_players_tags = players_frequent_tags(searched_players, counters)

    return compute_tags_similarities(players, searched_players_tags)


def recommend_teams_by_search(profile):
    searched_teams = profile.searched_teams.all()
    fav_team = profile.fav_team
    fav_player_team = profile.fav_player.team
    searched_players_teams = [p.team for p in profile.searched_players.all()]

    frequent_teams = set(
        searched_teams + searched_players_teams + [fav_player_team])

    recommendation = []
    for team in frequent_teams:
        if team != fav_team:
            recommendation.append(team)

    random.shuffle(recommendation)
    return recommendation[:10]


def dice_coefficient(set1, set2):
    return 2 * len(set1.intersection(set2)) / (len(set1) + len(set2))


def manhattan_distance(list1, list2):
    return sum(abs(list1[i] - list2[i]) for i in range(len(list1)))

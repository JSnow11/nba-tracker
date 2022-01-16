import random

from tracker.models import Player, Team


def get_player_stats(player):
    return [player.min_per_game, player.pts_per_game, player.field_goal,
            player.three_p_ptg, player.ft_ptg, player.reb_per_game,
            player.ast_per_game, player.tov_per_game, player.stl_per_game,
            player.blk_per_game]


def players_stats_mean(players, profile):
    mean = {"mpg": 0,
            "pts": 0,
            "fg": 0,
            "3p": 0,
            "ft": 0,
            "reb": 0,
            "ast": 0,
            "tov": 0,
            "stl": 0,
            "blk": 0
            }

    for player in players:
        count = profile.playersearchcounter_set.filter(
            player_id=player.id)[0].count

        mean["mpg"] += player.min_per_game * count
        mean["pts"] += player.pts_per_game * count
        mean["fg"] += player.field_goal * count
        mean["3p"] += player.three_p_ptg * count
        mean["ft"] += player.ft_ptg * count
        mean["reb"] += player.reb_per_game * count
        mean["ast"] += player.ast_per_game * count
        mean["tov"] += player.tov_per_game * count
        mean["stl"] += player.stl_per_game * count
        mean["blk"] += player.blk_per_game * count

    for key in mean:
        mean[key] /= len(players)

    print("VALUES: ", mean.values())
    return list(mean.values())


def compute_stats_similarities(players, search_player_mean):
    print('Computing search-player similarity matrix')
    return sorted([{"distance": manhattan_distance(get_player_stats(player), search_player_mean), "player": player} for player in players], key=lambda x: x["distance"])[:8]


def recommend_players_by_stats(profile):
    searched_players = profile.searched_players.all()

    players = Player.objects.all()
    searched_players_stat_mean = players_stats_mean(searched_players, profile)

    return compute_stats_similarities(players, searched_players_stat_mean)


def players_frequent_tags(searched_players, profile):
    frec = {}
    for player in searched_players:
        count = profile.playersearchcounter_set.filter(
            player_id=player.id)[0].count

        for tag in player.tags.all():
            if tag in frec.keys():
                frec[tag] = frec.get(tag, 0) + count
            else:
                frec[tag] = count

        frec[player.position] = frec.get(player.position, 0) + count

    return [k for k, v in sorted(frec.items(), key=lambda item: item[1], reverse=True)]


def compute_tags_similarities(players, search_frequent_tags):
    print('Computing tags-player similarity matrix')

    return sorted([{"value": dice_coefficient(set(player.tags.all()), set(search_frequent_tags)), "player": player} for player in players], key=lambda x: -x["value"])[:8]


def recommend_players_by_tags(profile):
    searched_players = profile.searched_players.all()

    players = Player.objects.all()
    searched_players_tags = players_frequent_tags(searched_players, profile)

    return compute_tags_similarities(players, searched_players_tags)


def recommend_teams_by_search(profile):
    searched_teams = list(profile.searched_teams.all())
    recommended_players_teams = [
        p["player"].team for p in recommend_players_by_stats(profile)] + [
        p["player"].team for p in recommend_players_by_tags(profile)]

    return list(set(recommended_players_teams).union(set(searched_teams)))[:8]


def dice_coefficient(set1, set2):
    return 2 * len(set1.intersection(set2)) / (len(set1) + len(set2))


def manhattan_distance(list1, list2):
    return sum(abs(list1[i] - list2[i]) for i in range(len(list1)))

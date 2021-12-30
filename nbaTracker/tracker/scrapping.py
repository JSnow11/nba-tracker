
from bs4 import BeautifulSoup as bs

from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options

import os
import ssl
if (not os.environ.get('PYTHONHTTPSVERIFY', '') and
        getattr(ssl, '_create_unverified_context', None)):
    ssl._create_default_https_context = ssl._create_unverified_context


official_nba_url = "https://es.global.nba.com/"
nba_teams_url = official_nba_url + "teamindex/"


chrome_options = Options()


def scrap_teams():
    with Chrome(options=chrome_options) as browser:

        browser.get(nba_teams_url)
        teams_soup = bs(browser.page_source, "html.parser")

        teams = []

        conferences = teams_soup.find(
            "div", class_="sib-list sib-team-list").findChildren("div", recursive=False)

        print(conferences)

        for c in conferences:
            conference_name = c.find("div").find("span").text.split(
                "Conferencia")[0].strip()
            print(conference_name)

            divisions = c.find_all("div", class_="division")

            for d in divisions:
                division_name = d.find("div", class_="division-label").text
                print(division_name)

                team_banners = d.find_all("div", class_="team")

                for banner in team_banners:
                    team_img = official_nba_url + \
                        banner.find("img", class_="team-img").attrs["src"]
                    team_name = banner.find("span", class_="name").text

                    team_url = official_nba_url + \
                        banner.find(
                            "a", class_="ng-isolate-scope").attrs["href"]

                    browser.get(team_url)
                    team_soup = bs(browser.page_source, "html.parser")

                    team_wins_losses = team_soup.find("div", class_="row").find(
                        "div", class_="hidden-sm nba-team-info-right").text

                    team_wins = team_wins_losses.split("V")[0].strip()
                    team_losses = team_wins_losses.split(
                        "-")[1].split("D")[0].strip()

                    teams.append({
                        "name": team_name,
                        "img_url": team_img,
                        "wins": team_wins,
                        "losses": team_losses,
                        "division": division_name,
                        "conference": conference_name
                    })

        return teams


def scrap_players():
    with Chrome(options=chrome_options) as browser:
        browser.implicitly_wait(1000)

        browser.get(nba_teams_url)
        teams_soup = bs(browser.page_source, "html.parser")

        players = []

        teams = teams_soup.find_all("div", class_="team")

        for t in teams:
            team_name = t.find("span", class_="name").text
            print("team: " + team_name)

            team_roster_url = official_nba_url + \
                t.find("a", string="Plantilla").attrs["data-ng-href"]
            browser.get(team_roster_url)
            roaster_soup = bs(browser.page_source, "html.parser")

            roaster_players = roaster_soup.find(
                "div", class_="nba-stat-table__overflow").find("tbody").find_all("tr")

            for p in roaster_players:
                player_name = "".join([n.text.strip() + " " for n in p.find(
                    "a", class_="player-name").find_all("span")])
                print("player: " + player_name)
                player_img = p.find("img", class_="player-img").attrs["src"]

                player_data = p.find_all("td")

                player_position = player_data[1].text
                player_number = player_data[4].text

                player_url = official_nba_url + p.find("a").attrs["href"]

                browser.get(player_url)
                player_soup = bs(browser.page_source, "html.parser")

                player_stats = player_soup.find(
                    "tr", class_="ng-scope").find_all("td")
                player_mpp = player_stats[4].text
                player_fg = player_stats[5].text
                player_repp = player_stats[10].text
                player_app = player_stats[11].text
                player_ropp = player_stats[12].text
                player_bpp = player_stats[13].text
                player_ppp = player_stats[16].text

                players.append({
                    "name": player_name,
                    "img_url": player_img,
                    "position": player_position,
                    "number": player_number,
                    "min_per_game": player_mpp,
                    "pts_per_game": player_ppp,
                    "field_goal": player_fg,
                    "reb_per_game": player_repp,
                    "ast_per_game": player_app,
                    "rob_per_game": player_ropp,
                    "blk_per_game": player_bpp,
                    "team": team_name
                })


if __name__ == "__main__":
    print("scrapping")
    scrap_teams()

    scrap_players()

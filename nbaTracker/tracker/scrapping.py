
from bs4 import BeautifulSoup as bs

from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

import time
import os
import ssl
if (not os.environ.get('PYTHONHTTPSVERIFY', '') and
        getattr(ssl, '_create_unverified_context', None)):
    ssl._create_default_https_context = ssl._create_unverified_context


official_nba_url = "https://es.global.nba.com/"
official_nba_standings_url = "https://www.nba.com/standings?GroupBy=div&Season=2021-22&Section=overall"
official_nba_stats_url = "https://www.nba.com/stats/players/traditional/?sort=PLAYER_NAME&dir=-1"
nba_teams_url = official_nba_url + "teamindex/"

official_nba_players_url = "https://www.nba.com/players"

chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument('window-size=1920x1080')
chrome_options.add_argument("--incognito")
chrome_options.add_argument('disable-blink-features=AutomationControlled')
chrome_options.add_argument('user-agent=Type user agent here')


def scrap_div_teams(teams, divisions, division_name, div_table, conference_name):
    division_teams = div_table.find("tbody").find_all("tr")

    for t in division_teams:
        team_data = t.find_all("td")

        title = team_data[0].find(
            "div", class_="ml-2").text.split(" ")

        print(title)

        team_name = title[0] + " " + title[1] +  \
            (" " + title[2] if len(title) == 5 else "")
        team_abbreviation = title[-2]
        print(team_abbreviation + "- " + team_name)

        team_img = team_data[0].find("img").attrs["src"]

        team_wins = team_data[1].text
        team_losses = team_data[2].text

        print("{}, {}".format(team_wins, team_losses))
        teams.append({
            "name": team_name,
            "abbreviation": team_abbreviation,
            "img_url": team_img,
            "wins": team_wins,
            "losses": team_losses,
            "division": division_name,
            "conference": conference_name
        })


def scrap_teams():
    with Chrome(options=chrome_options) as browser:

        print("\nScrapping teams...")
        browser.get(official_nba_standings_url)

        time.sleep(2)
        teams_soup = bs(browser.page_source, "html.parser")

        teams = []
        conferences = []
        divisions = []

        division_titles = teams_soup.find_all("h5", class_="h5")
        print(division_titles)
        division_tables = teams_soup.find_all(
            "div", class_="MockStatsTable_statsTable__2edDg")

        conference_name = "Eastern"
        conferences.append(conference_name)
        print(conference_name)
        for d in range(0, 3):
            division_name = division_titles[d].text.split(" Division")[
                0].strip()
            divisions.append({"division": division_name,
                              "conference": conference_name})

            scrap_div_teams(teams, divisions, division_name,
                            division_tables[d], conference_name)

        conference_name = "Western"
        conferences.append(conference_name)
        print(conference_name)
        for d in range(3, 6):
            division_name = division_titles[d].text.split(" Division")[
                0].strip()
            divisions.append({"division": division_name,
                              "conference": conference_name})

            scrap_div_teams(teams, divisions, division_name,
                            division_tables[d], conference_name)

        return teams, conferences, divisions


def scrap_players():
    with Chrome(options=chrome_options) as browser:

        print("\nScrapping players...")
        browser.get(official_nba_stats_url)

        time.sleep(1)
        el = browser.find_element(
            By.CLASS_NAME, 'stats-table-pagination__select')
        for option in el.find_elements(By.TAG_NAME, 'option'):
            if option.text == 'All':
                option.click()  # select() in earlier versions of webdriver
                break

        teams_soup = bs(browser.page_source, "html.parser")

        players = []

        player_rows = teams_soup.find(
            "div", class_="nba-stat-table__overflow").find("tbody").find_all("tr")

        for pw in player_rows:
            player_data = pw.find_all("td")

            player_name = player_data[1].text.strip()
            team_abbr = player_data[2].text.strip()

            print(team_abbr + " - " + player_name)

            player_mpp = float(player_data[7].text.strip())
            player_ppp = float(player_data[8].text.strip())
            player_fg = float(player_data[11].text.strip())
            player_3p = float(player_data[14].text.strip())
            player_ft = float(player_data[17].text.strip())
            player_rpp = float(player_data[20].text.strip())
            player_app = float(player_data[21].text.strip())
            player_topp = float(player_data[22].text.strip())
            player_spp = float(player_data[23].text.strip())
            player_bpp = float(player_data[24].text.strip())
            player_plus_minus = float(player_data[-1].text.strip())

            print("{}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}".format(
                player_mpp, player_ppp, player_fg, player_3p, player_ft, player_rpp, player_app, player_topp, player_spp, player_bpp, player_plus_minus))

            players.append({
                "name": player_name,
                "min_per_game": player_mpp,
                "pts_per_game": player_ppp,
                "field_goal": player_fg,
                "three_p_ptg": player_3p,
                "ft_ptg": player_ft,
                "reb_per_game": player_rpp,
                "ast_per_game": player_app,
                "tov_per_game": player_topp,
                "stl_per_game": player_spp,
                "blk_per_game": player_bpp,
                "plus_minus": player_plus_minus,
                "team": team_abbr
            })

        browser.get(official_nba_players_url)
        time.sleep(1)

        el = browser.find_element(
            By.XPATH, '//*[@id="__next"]/div[2]/div[3]/section/div/div[2]/div[1]/div[7]/div/div[3]/div/label/div/select')
        for option in el.find_elements(By.TAG_NAME, 'option'):
            if option.text == 'All':
                option.click()  # select() in earlier versions of webdriver
                break

        players_soup = bs(browser.page_source, "html.parser")

        player_rows = players_soup.find(
            "div", class_="MockStatsTable_statsTable__2edDg").find("tbody").find_all("tr")

        for pw in player_rows:
            player_data = pw.find_all("td")

            player_img = player_data[0].find("img").attrs["src"]
            player_name_texts = player_data[0].find_all("p", class_="t6")
            player_name = player_name_texts[0].text.strip(
            ) + " " + player_name_texts[1].text.strip()
            player_number = player_data[2].text.strip()
            player_position = player_data[3].text.strip()
            player_country = player_data[7].text.strip()
            team_abbr = player_data[1].text.strip()

            print(team_abbr + " - " + player_name)
            player_dic_index = next((i for i, p in enumerate(players) if p and p["name"] ==
                                     player_name and p["team"] == team_abbr), None)

            if(player_dic_index):
                new_items = {}
                new_items["img"] = player_img
                new_items["number"] = player_number
                new_items["position"] = player_position
                new_items["country"] = player_country

                new_items.update(players[player_dic_index])
                players[player_dic_index] = new_items

        print(players)
        return players


if __name__ == "__main__":
    print("testing scrapping locally...")
    # scrap_teams()
    # scrap_players()

import config as cf
from tqdm import tqdm
import argparse
import requests
from selenium import webdriver
from bs4 import BeautifulSoup
from dateutil.parser import parse
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service


def extractTeamsURLs(league_url):
    """
    this function extract teams url out of league home page
    :param league_url: league url as a string
    :return: all teams urlss unique and alphabetically sorted in a list
    """
    team_list = []
    options = getDriverOption()
    driver = webdriver.Chrome(options=options)
    driver.get(league_url)  # mimicking human behaviour and opening league url
    team_html = BeautifulSoup(driver.page_source, 'html.parser')  # getting the source with selenium, parsing with bs4
    driver.close()
    # looking after all teams urls
    all_anchor = team_html.find_all('a')
    for anchor in all_anchor:
        hrefs = anchor.get('href')
        hrefs_list = str(hrefs).split()
        for href in hrefs_list:
            if '/team/football/' in href:
                team_list.append('https://www.sofascore.com' + str(href))
    sorted_teams = sorted(list(set(team_list)))  # sorting and removing duplicates
    return sorted_teams

# # helper function to get driver options
def getDriverOption():
    options = webdriver.ChromeOptions()
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    return options

def getTeamPlayerInfo(league='epl'):
    league_name = cf.TOP_LEAGUES_URLS[league].split("/")[-2]
    teams = extractTeamsURLs(cf.TOP_LEAGUES_URLS[league])  # extracting teams out of leagues tables
    return teams
    # print("\ngetting teams from " + league_name)  # printing for user "loading" in addition to tqdm
    # # db_control.write_league([league_name, len(teams)])
    # watch = tqdm(total=len(teams), position=0)
    # for team_url in teams:  # iterating all teams urls
    #     team_name = team_url.split('/')[-2]
    #     manager_info = extract_mgr_info(team_url)
    #     players_list = hp.extract_players_urls(team_url)  # extracting player url which
    #     db_control.write_teams([team_name, len(players_list)], league_name)
    #     db_control.write_players(players_list, team_name)
    #     db_control.write_manager(manager_info, team_name)
    #     extra_team_info = api.get_info_from_api(team_name)  # retrieving external data from the api
    #     db_control.write_team_extras(extra_team_info, team_name)  # writing this data into the database
    #     watch.update(1)

def main():
    teams_url = getTeamPlayerInfo()
    print(teams_url)

    # need dataframe with fields below
    # team,	player,	competition,	game date,	home team,	away team,	home score,	player goal,	player penalty goal,	player assist,	player yellow card,	player red card


if __name__ == '__main__':
    main()


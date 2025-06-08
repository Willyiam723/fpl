import config as cf
from tqdm import tqdm
import argparse
import requests
from selenium import webdriver
from bs4 import BeautifulSoup
from dateutil.parser import parse
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
import pandas as pd


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

def extractPlayersURLs(team_url):
    """
    this function fet url of a team and extract all of the players url list out of it.
    then it send the player url to extract player info func to get all info about the player
    :param team_url: a url to a team page as a string
    """
    players_list = []
    options = getDriverOption()
    driver = webdriver.Chrome(options=options)
    driver.get(team_url)
    team_html = BeautifulSoup(driver.page_source, 'html.parser')
    driver.close()

    # look for the player info inside the page
    all_anchor = team_html.find_all('a')
    for anchor in all_anchor:
        hrefs = anchor.get('href')
        hrefs_list = str(hrefs).split()
        for href in hrefs_list:
            if '/player/' in href:
                players_list.append('https://www.sofascore.com' + str(href))
    sorted_players = sorted(list(set(players_list)))  # sorting and removing duplicates
    return sorted_players

def extractPlayerDataframe(player_url, team_name, player_name):
    """
    this function fet dataframe of a player and extract all of the players plast games out of it.
    :param player_url: a url to a player as a string
    """

    df = pd.DataFrame(columns=['team', 'player', 'competition', 'game date', 'home team', 'away team', 
                               'home score', 'player goal', 'player penalty goal', 'player assist', 
                               'player yellow card', 'player red card'])
    options = getDriverOption()
    driver = webdriver.Chrome(options=options)
    driver.get(player_url)
    player_html = BeautifulSoup(driver.page_source, 'html.parser')

    #build dataframe...




def getTeamPlayerDataframe(league='epl'):
    league_name = cf.TOP_LEAGUES_URLS[league].split("/")[-2]
    teams = extractTeamsURLs(cf.TOP_LEAGUES_URLS[league])  # extracting teams out of leagues tables

    print('\ngetting teams from ' + league_name)  # printing for user "loading" in addition to tqdm
    watch = tqdm(total=len(teams), position=0)
    df = pd.DataFrame(columns=['team', 'player', 'competition',	'game date', 'home team', 'away team', 
                               'home score', 'player goal', 'player penalty goal', 'player assist', 
                               'player yellow card', 'player red card'])
    for team_url in teams:  # iterating all teams urls
        team_name = team_url.split('/')[-2]
        players_list = extractPlayersURLs(team_url)  # extracting player url which
        for player_url in players_list:  # iterating all players urls
            player_name = player_url.split('/')[-2]
            df_player = extractPlayerDataframe(player_url, team_name, player_name)
            df = pd.concat([df, df_player], axis=0)
        print('\n getting player dataframe from' + team_name)
        watch.update(1)
    return df

def main():
    teams_url = getTeamPlayerDataframe()
    # print(teams_url)

    # need dataframe with fields below
    # team,	player,	competition,	game date,	home team,	away team,	home score,	player goal,	player penalty goal,	player assist,	player yellow card,	player red card


if __name__ == '__main__':
    main()


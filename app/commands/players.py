import click 
import requests
import json
import os

from datetime import datetime
from app.log import logger
from app.settings import API_KEY as api_key
from time import sleep

def verify_requests(url):
    status = requests.get(url).status_code

    if status == 429:
        logger.info('Rate limit exceeded')
        while status == 429:
            logger.info('Wainting')
            sleep(10)
            status = requests.get(url).status_code

    if status == 200:
        return requests.get(url).json()

def get_players_tier(server, tier):
    ''' LEAGUE-V4'''
    url =  f'https://{server}.api.riotgames.com/lol/league/v4/{tier}/by-queue/RANKED_SOLO_5x5?api_key={api_key}'
    json_request = verify_requests(url) 

    return json_request


def get_dim_players(server, tier):
    players = get_players_tier(server, tier)
    #summonersIds = [d["summonerId"] for d in players['entries']]
    
    data = []
    for player in players['entries']: 
        summonerId = player["summonerId"]
        url = f'https://{server}.api.riotgames.com/lol/summoner/v4/summoners/{summonerId}?api_key={api_key}'

        player_infos = verify_requests(url) 
        player.update(player_infos)
        data.append(player)
    
    build_dim_players(server, tier, data)

def build_dim_players(server, tier, data):
    json_file = {
        'players' : data
    }
    
    date = datetime.today().strftime('%Y-%m-%d')
    path = f'C:\\Users\\Andrey-PC\\Desktop\\TCC\\datalake\\{tier}\\{server}\\{date}'

    if not os.path.exists(path):
        os.makedirs(path)

    with open(f'{path}\\players.json', "w") as outfile:
        json.dump(json_file, outfile)

@click.command(help='')
def run():
    server = 'kr'
    tier = 'challengerleagues'
    get_dim_players(server, tier)

if __name__ == '__main__':
    run()
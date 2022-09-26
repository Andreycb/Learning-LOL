import click 
import requests
import json
import os
import re

from time import sleep
from app.commands.players import verify_requests
from datetime import datetime
from app.log import logger
from app.settings import API_KEY as api_key
from app.mongo import distinct_mongo, read_mongo, save_mongo, search_mongo

def define_region(server):
    if server == 'BR1':
        region = 'americas'
    if server == 'KR':
        region = 'asia'
    
    return region


def verify_exists():
    if search_mongo():
        return True

    return False


def define_data():
    id = distinct_mongo('LeagueOfLegends', 'IdMatches', 'MatcheId')
    matches = distinct_mongo('LeagueOfLegends', 'Matches', 'metadata.matchId')
    data = list(set(id) - set(matches))
 
    return data

def get_matches():
    data = define_data()

    for matche in data:
        id = matche['MatcheId']

        if search_mongo('LeagueOfLegends', 'Matches', str(id)):
            logger.info("Essa partida ja está na base")
            continue

        server = re.search('[a-zA-Z]+', id).group()
        region = define_region(server)

        url = f'https://{region}.api.riotgames.com/lol/match/v5/matches/{id}?api_key={api_key}'
        infos = verify_requests(url)
        save_mongo('LeagueOfLegends', 'Matches', infos)


@click.command(help='')
def run():
    get_matches()

if __name__ == '__main__':
    run()
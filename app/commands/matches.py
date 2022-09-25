import click 
import requests
import json
import os


from app.commands.players import verify_requests
from datetime import datetime
from app.log import logger
from app.settings import API_KEY as api_key
from time import sleep

def define_region(server):
    if server == 'br1':
        region = 'americas'
    if server == 'kr':
        region = 'asia'
    
    return region


def read_dim_players(server, tier):
    f = open(f'C:\\Users\\Andrey-PC\\Desktop\\TCC\\datalake\\{tier}\\{server}\\2022-08-18\\players.json') #Dinamizar
    data = json.load(f)
    
    return data


def get_matches(server, data):
    region = define_region(server)

    for player in data['players']:
        puuid = player['puuid']

        init = 0
        while True:
            url = f'https://{region}.api.riotgames.com/lol/match/v5/matches/by-puuid/{puuid}/ids?api_key={api_key}&type=ranked&start={init}&count=100'
            matches = verify_requests(url)
            init +=100

            if len(matches) == 0:
                break
            
            build_matches_file(matches, region)


def get_matches_info():
    pass


def build_matches_file(matches,region):
    path = f'C:\\Users\\Andrey-PC\\Desktop\\TCC\\datalake\\matches\\{region}'

    if not os.path.exists(path):
        os.makedirs(path)

    with open(f'{path}\\matches.txt', 'a') as f:
        for matcheId in matches:
            f.write(f'{matcheId}\n')


def file_to_list(path):
    # matches = []
    # file_object = open(path, "r")
    # matches = file_object.read().splitlines()
    # file_object.close()
    # return list(filter(None, pd.unique(matches).tolist()))
    pass

@click.command(help='')
def run():

    data = read_dim_players('br1', 'challengerleagues')
    get_matches('br1', data)

if __name__ == '__main__':
    run()
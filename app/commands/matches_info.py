import click 
import re

from app.commands.players import verify_requests
from app.log import logger
from app.settings import API_KEY as api_key
from app.mongo import distinct_mongo, save_mongo, search_mongo, read_mongo, delete_register

def define_region(server):
    if server == 'BR1' or server == 'NA1':
        region = 'americas'
    if server == 'KR':
        region = 'asia'
    
    return region


def define_data():
    id = distinct_mongo('LeagueOfLegends2', 'IdMatches', 'MatcheId')
    matches = distinct_mongo('LeagueOfLegends2', 'Matches', 'metadata.matchId')
    data = list(set(id) - set(matches))

    return data


def get_matches():
    data = data = read_mongo('LeagueOfLegends2', 'IdMatches_NA')
    for id in data:
        try:
            # if search_mongo('LeagueOfLegends', 'Matches', 'metadata.matchId', str(id)):
            #     logger.info("Essa partida ja está na base")
            #     continue
            
            id_matche = id['MatcheId']
            server = "NA1"
            region = define_region(server)

            url = f'https://{region}.api.riotgames.com/lol/match/v5/matches/{id_matche}?api_key={api_key}'
            infos = verify_requests(url)

            save_mongo('LeagueOfLegends2', 'Matches_NA', infos)

            delete_register('LeagueOfLegends2', 'IdMatches_NA', id)
        except:
            continue


@click.command(help='')
def run():
    get_matches()

if __name__ == '__main__':
    run()
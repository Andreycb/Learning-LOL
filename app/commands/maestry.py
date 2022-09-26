import click 

from app.commands.players import verify_requests
from app.log import logger
from app.settings import API_KEY as api_key
from app.mongo import read_mongo, save_mongo

def get_maestry():
    data = read_mongo('LeagueOfLegends', 'Players')
    for player in data:
        region = player['region']
        id = player['id']
        url = f'https://{region}.api.riotgames.com/lol/champion-mastery/v4/champion-masteries/by-summoner/{id}?api_key={api_key}'
        infos = verify_requests(url)
        save_mongo('LeagueOfLegends', 'Maestry', infos)


@click.command(help='')
def run():
    get_maestry()

if __name__ == '__main__':
    run()
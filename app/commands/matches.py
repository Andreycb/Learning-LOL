import click 

from time import sleep
from app.commands.players import verify_requests
from app.settings import API_KEY as api_key
from app.mongo import read_mongo, save_mongo, delete_register

def define_region(server):
    if server == 'br1':
        region = 'americas'
    if server == 'kr':
        region = 'asia'
    
    return region

def build_to_json(matche):
    data = {'MatcheId': matche}

    return data 


def get_id_matches():
    data = read_mongo('LeagueOfLegends', 'Players')
    for player in data:
        server = player['region']
        puuid = player['puuid']
        region = define_region(server)
        init = 0
        while True:
            url = f'https://{region}.api.riotgames.com/lol/match/v5/matches/by-puuid/{puuid}/ids?api_key={api_key}&type=ranked&start={init}&count=100'
            matches = verify_requests(url)
            init +=100

            if len(matches) == 0:
                break

            for matche in matches:
                save_mongo('LeagueOfLegends', 'IdMatches', build_to_json(matche))

        delete_register('LeagueOfLegends', 'Players', player)


@click.command(help='')
def run():
    get_id_matches()

if __name__ == '__main__':
    run()
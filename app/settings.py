from dotenv import load_dotenv
import os

load_dotenv()

API_KEY = os.environ.get("API_KEY")

SERVERS = ['BR1', 'EUN1', 'EUNW1', 'JP1', 'KR', 'LA1', 'LA2', 'NA1', 'OC2', 'RU', 'TR1']

TIERS = ['challengerleagues', 'masterleagues', 'grandmasterleagues']

REGIONS = {'AMERICAS': ['BR1'],
           'ASIA': [],
           'EUROPE': [],
           'SEA': []}
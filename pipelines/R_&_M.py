from asyncio import subprocess

import pandas as pd
import requests
from pandas import json_normalize
import os
from dotenv import load_dotenv

load_dotenv()

all_cast =  []

url = os.getenv("API_URL") + os.getenv("API_ENDPOINT")

while url:
    response = requests.get(url)

    if response.status_code ==  200:
       data = response.json()
       all_cast.extend(data['results'])
       url=data['info']['next']
    
df = pd.json_normalize(all_cast)

from sqlalchemy import create_engine

engine = create_engine(os.getenv("sql_engine"))

df.to_sql('rick_morty_cast_analysis', engine, if_exists='replace', index=False)
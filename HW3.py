#HW3

import requests
import redis 
import json

redis_host = 'redis-16990.c282.east-us-mz.azure.cloud.redislabs.com'
redis_port = 16990
redis_password = '1BUZsxdiUGQ5yAiS2QsTDQQSYworEvEM'

r = redis.Redis(host=redis_host, port=redis_port, password=redis_password)

url = "https://nba-team-stats.p.rapidapi.com/teamStats"

json_data = []

i  = ["2020", "2021", "2022", "2023"]
for i in i:
    querystring = {"leagueYear":i,"team":"76ers"}

    headers = {
	     "X-RapidAPI-Key": "6d0eed541cmsh7ff9a881cf8927bp1882dfjsn193c7fb63a4d",
	     "X-RapidAPI-Host": "nba-team-stats.p.rapidapi.com"
    }

    response = requests.get(url, headers=headers, params=querystring)
    print(response.json())

    
print("Done")
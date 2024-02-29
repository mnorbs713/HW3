#HW3

import requests
import redis 
import json
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

class API:
    """
    API Class
    Vaiables:
    - url (str): URL to API
    """
    def __init__(self, url):
        self.url = url
    def get_data(self, headers, params):
        """
        Uses headers and params to return API data.
        Parameters:
        - headers (str): header for APIUkeys.
        - params (str): parameters for query.
        Returns:
        response.json(): JSON data using the params and header with the API.
        """
        response = requests.get(url, headers=headers, params=params)
        if response.status_code == 200:
            return response.json()
        else:
            return None
    
class Redis:
    """
    Redis Class.
    Attributes:
    - host (str): host for redis
    - port (int): port for redis.
    - password (str): password for redis.
    """
    def __init__(self, host, port, password):
        self.r = redis.StrictRedis(host=host, port=port, password=password) 
    def set_json(self, key, data):
        """
        converts data to RedisJSON.
        Parameters:
        - key (bytes): key for data dictionary.
        - data (dict): data dictionary holding data.
        """
        json_data = json.dumps(data)
        self.r.set(key, json_data)
    def get_json(self, key):
        """
        Gets JSON data from RedisJSON.
        Parameters:
        - key (bytes): key to data dictionary.
        Returns:
        If json_data exists, put JSON data into a data dictionary. 
        """
        json_data = self.r.get(key)
        if json_data is not None:
            return json.loads(json_data)
        else:
            return None
    def get_keys(self):
        """
        retrieves keys from RedisJSON.
        Returns:
        return the JSON data to a data dictionary. 
        """
        return self.r.keys()
    
if __name__ == "__main__":

    "Necessary API info"
    url = "https://nba-team-stats.p.rapidapi.com/teamStats"
    headers = {
	     "X-RapidAPI-Key": "6d0eed541cmsh7ff9a881cf8927bp1882dfjsn193c7fb63a4d",
	     "X-RapidAPI-Host": "nba-team-stats.p.rapidapi.com"
    }
    data_dict = {}
    
    
    "pull API data"
    api_client = API(url)
    if len(data_dict) == 0:
        for i in range(2019,2024):
           params = {"leagueYear":str(i),"team":"76ers"}
           data_dict[i] = api_client.get_data(headers,params)
        
    "Necessary Redis Info"
    host = 'redis-16990.c282.east-us-mz.azure.cloud.redislabs.com'
    port = 16990
    password = '1BUZsxdiUGQ5yAiS2QsTDQQSYworEvEM'
    redis_dict = {}
    redis_client = Redis(host, port, password)
    
    "take data and place into redis"
    for key in data_dict:
        redis_client.set_json(key, data_dict[key])
    
    "Retrieve data from redis"
    key_list = redis_client.get_keys() 
    for key in key_list: 
        redis_dict[key] = redis_client.get_json(key)

    "set up data for analysis"
    keys = list(redis_dict.keys())
    leagueyear_values  = [redis_dict[key].get('leagueYear',None)for key in keys]
    point_values_str = [redis_dict[key]["stats"]["Philadelphia 76ers"]["Per Game"].get('PTS',None)for key in keys]
    point_values_flt = [float(x) for x in point_values_str]
    opp_point_values_str = [redis_dict[key]["stats"]["Philadelphia 76ers"]["Per Game Opponent"].get('PTS',None)for key in keys]
    opp_point_values_flt = [float(x) for x in opp_point_values_str]
    attendance_per_game_str = [redis_dict[key]["stats"]["Philadelphia 76ers"]["Advanced"].get('Attend./G',None)for key in keys]
    attendance_per_game_str_no_comma = [s.replace(',','')for s in attendance_per_game_str]
    attendance_per_game_flt = [float(x) for x in attendance_per_game_str_no_comma]
    df = pd.DataFrame({'year': leagueyear_values, 'Pointspergame': point_values_flt, 'OppPointspergame':opp_point_values_flt, 'attendancepergame':attendance_per_game_flt})
    df = df.sort_values(by='year')
    df = df.reset_index(drop=True)
    
    "plot of 76ers points per game by year"
    plt.bar(df['year'],df['Pointspergame'],width=.5)
    plt.ylim(100,120)
    plt.xlabel('Year')
    plt.ylabel('Points per Game')
    plt.title('Points per Game for Philadelphia 76ers')
    
    "plot of 76ers Opponents points per game by year"
    plt.bar(df['year'],df['OppPointspergame'],width=.5)
    plt.ylim(100,120)
    plt.xlabel('Year')
    plt.ylabel('Points per Game')
    plt.title('Points per Game for Philadelphia 76ers Opponents')
    
    "plot of &6ers attendance per game by year"
    plt.bar(df['year'],df['attendancepergame'],width=.5)
    plt.ylim(1000,21000)
    plt.xlabel('Year')
    plt.ylabel('Attendance per Game')
    plt.title('Attendance per Game Philadelphia 76ers')
    
    
    
print("Done")
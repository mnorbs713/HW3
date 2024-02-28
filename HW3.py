#HW3

import requests
import redis 
import json
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

class APIStuff:
    """
    A class for handling the API.
    Attributes:
    - url (str): The url for the API.
    """
    def __init__(self, url):
        self.url = url
    def get_data(self, headers, params):
        """
        Uses headers and params to return API data.
        Parameters:
        - headers (str): header that holds API keys.
        - params (str): params for the API query.
        Returns:
        response.json(): JSON data using the params and header with the API.
        """
        response = requests.get(url, headers=headers, params=params)
        if response.status_code == 200:
            return response.json()
        else:
            return None
    
class RedisStuff:
    """
    A class for handling Redis.
    Attributes:
    - host (str): host name for connecting to Redis.
    - port (int): port number for connecting to Redis.
    - password (str): password for connecting to Redis.
    """
    def __init__(self, host, port, password):
        self.r = redis.StrictRedis(host=host, port=port, password=password) 
    def set_json(self, key, data):
        """
        Sets JSON data to RedisJSON.
        Parameters:
        - key (bytes): key for the data dictionary.
        - data (dict): data dictionary holding API data.
        """
        json_data = json.dumps(data)
        self.r.set(key, json_data)
    def get_json(self, key):
        """
        Gets JSON data from RedisJSON.
        Parameters:
        - key (bytes): key for the data dictionary.
        Returns:
        If the json_data exists, return the JSON data to a data dictionary. 
        """
        json_data = self.r.get(key)
        if json_data is not None:
            return json.loads(json_data)
        else:
            return None
    def get_keys(self):
        """
        Gets keys from RedisJSON.
        Returns:
        If the json_data exists, return the JSON data to a data dictionary. 
        """
        return self.r.keys()
    
if __name__ == "__main__":

    url = "https://nba-team-stats.p.rapidapi.com/teamStats"
    headers = {
	     "X-RapidAPI-Key": "239f222809msha2e4818a47c0fdfp19a3e4jsna22b27732628",
	     "X-RapidAPI-Host": "nba-team-stats.p.rapidapi.com"
    }
    data_dict = {}
    api_client = APIStuff(url)
    if len(data_dict) == 0:
        for i in range(2019,2024):
           params = {"leagueYear":str(i),"team":"76ers"}
           data_dict[i] = api_client.get_data(headers,params)
        
        
    host = 'redis-16990.c282.east-us-mz.azure.cloud.redislabs.com'
    port = 16990
    password = '1BUZsxdiUGQ5yAiS2QsTDQQSYworEvEM'
    redis_dict = {}
    redis_client = RedisStuff(host, port, password)
    
    for key in data_dict:
        redis_client.set_json(key, data_dict[key])
    
    key_list = redis_client.get_keys() 
    for key in key_list: 
        redis_dict[key] = redis_client.get_json(key)

    keys = list(redis_dict.keys())
    leagueyear_values  = [redis_dict[key].get('leagueYear',None)for key in keys]
    point_values = [redis_dict[key]["stats"]["Philadelphia 76ers"]["Per Game"].get('PTS',None)for key in keys]
    df = pd.DataFrame({'year': leagueyear_values, 'Pointspergame': point_values})

    plt.plot(df['year'], df['Pointspergame'], marker = 'o')
    
print("Done")
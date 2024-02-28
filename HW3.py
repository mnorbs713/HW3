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
	     "X-RapidAPI-Key": "6d0eed541cmsh7ff9a881cf8927bp1882dfjsn193c7fb63a4d",
	     "X-RapidAPI-Host": "nba-team-stats.p.rapidapi.com"
    }
    data_dict = {}
    api_client = APIStuff(url)
    
    i  = ["2019", "2020", "2021", "2022", "2023"]
    
    if len(data_dict) == 0:
        for i in i:
            params = {"leagueYear":i,"team":"76ers"}
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

    
print("Done")
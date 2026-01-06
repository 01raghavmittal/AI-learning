'''
Docstring for Ai Agent.lab5


Function Calling with Azure Ai agents

 
'''
import requests
import os, time
import json

from dotenv import load_dotenv
load_dotenv()

weather_api_key=os.getenv('OPEN_WEATHER_API_KEY')

def get_weather(loacation):

    url= "" + loacation + ""
    response=requests.get(url)
    get_response=response.json
    latitude=response[0]['lat']
    longitude=response[0]['lon']

    url_final="" + str(latitude) +"&lon="+str(longitude)+"&appi"

    final_response=requests.get(url_final)
    final_response_json=final_response.json
    weather= final_response_json['weather'][0]['description']
    return weather

def get_user_info(user_id:str=None)->str:

    mock_users ={
        1:{"name":"Alice","email":"Alice@example.com"},
        2:{"name":"bob","email":"bob@example.com"},
        3:{"name":"charlie","email":"charlie@example.com"},
    }
    user_infor=mock_users.get(user_id,{'error':"user not found."})
    return json.dumps({'user_info':user_infor})

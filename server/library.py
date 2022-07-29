import requests
import os
from dotenv import load_dotenv


class Summoner: 

    def __init__(self, name):
        self.keyparam = f'?api_key={os.getenv('API_KEY')}'
        self.name = name

    def nameToId(self): #Gets the name and returns a ID
        response = requests.get(f"https://na1.api.riotgames.com/lol/summoner/v4/summoners/by-name/{self.name}{self.keyparam}").json()
        return response['id']

    def champMastery(self):
        response = requests.get(f"https://na1.api.riotgames.com/lol/champion-mastery/v4/champion-masteries/by-summoner/{self.nameToId()}{self.keyparam}").json()
        return response
        
    def sumstats(self):
        pass #return stats


test = Summoner("WarpWing")

print(test.champMastery())
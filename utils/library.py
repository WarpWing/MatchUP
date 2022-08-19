from unicodedata import name
import requests
import os
from dotenv import dotenv_values
import itertools
from rich.tree import Tree
from rich import *
config = dotenv_values(".env")

class Summoner: 

    def __init__(self, name):
        self.keyparam = f'?api_key=' + config['API_KEY'] #Is this bad code? Yes. Does it work? Yes. Is it a possible security risk? Idk. I just leave it alone and don't question it.
        self.name = name
        self.latestVersion = requests.get('https://ddragon.leagueoflegends.com/api/versions.json').json()[0]

    def nameToId(self): #Gets the name and returns a ID
        response = requests.get(f"https://na1.api.riotgames.com/lol/summoner/v4/summoners/by-name/{self.name}{self.keyparam}").json()
        return response['id']


    def idToChamp(self,id: int):
        response = requests.get("http://ddragon.leagueoflegends.com/cdn/6.24.1/data/en_US/champion.json").json()

        champInfo = response['data']

        champNames, champValues = list(champInfo.keys()), list(champInfo.values())
        
        #Is this extremely inefficent? Can I just make a sorted json string to parse from instead? Yes. Will I? In the future. Don't judge me.
        for count, champ in enumerate(list(champInfo.keys()), 0):  
            if champValues[count]['key'] == str(id):
                return champ

    def champMastery(self):
        response = requests.get(f"https://na1.api.riotgames.com/lol/champion-mastery/v4/champion-masteries/by-summoner/{self.nameToId()}{self.keyparam}").json()
        return response


    def getRanked(self):
        response = requests.get(f"https://na1.api.riotgames.com/lol/league/v4/entries/by-summoner/{self.nameToId()}{self.keyparam}").json()
        return list(response)[0]
        
    def sumstats(self):
        main = Tree("[green]WarpWing's Summoner Stats")
        ranked = main.add("[green]WarpWing's Ranked Stats")
        ranked.add(f"[magenta]Division: {self.getRanked()['tier'].capitalize()} {self.getRanked()['rank']}")
        ranked.add(f"[cyan]LP: {self.getRanked()['leaguePoints']}")
        ranked.add(f"[green]Wins: {self.getRanked()['wins']}")
        ranked.add(f"[red]Losses: {self.getRanked()['losses']}")
        ranked.add(f"[yellow]Win/Loss Ratio: {(self.getRanked()['wins'] / self.getRanked()['losses']):.2f}")
        return main

        


test = Summoner("WarpWing")

print(test.sumstats())

import random
import json
import numpy as np
import pandas as pd
from dataclasses import dataclass
from typing import List


class Game:
    def __init__(self, players):
        self.grid = []
        self.players = players
        self.turn = 0
        self.properties = {}

    def roll(self, player):
        roll = random.randint(1, 6) + random.randint(1, 6)
        self.players[player.title].position += roll
        self.players[player.title].position %= 40

    def buy(self, player, property):
        if self.players[player.title].money >= self.properties[property.title].price:
            self.players[player.title].properties.update({property.title: self.properties[property.title]})
            self.players[player.title].money -= self.properties[property.title].price

    def to_json(self):
        out = {
            "turn": self.turn
        }
        for player in list(self.players.values()):
            out.update(player.to_json())
        print(out)
        with open("sample.json", "w") as outfile:
            json.dump(out, outfile)


class Tile:
    def __init__(self, title, position):
        self.title = title
        self.position = position


@dataclass
class Property:
    title: str
    price: int
    rent_no_set: int
    rent_color_set: int
    rent_1_house: int
    rent_2_house: int
    rent_3_house: int
    rent_4_house: int
    rent_hotel: int
    building_cost: int
    mortgage: int
    unmortgage: int
    color: str

@dataclass
class Player:
    title: str
    piece: str
    position: int
    money: int
    properties: List[Property]



"""
Reads property data from csv and lets you index data by column(Type of value like price)
or row (Property name like Board Walk)
"""
data = pd.read_csv("properties.csv", index_col=0)
print(data.iloc[len(data)-1])
board = Property(data.index.values[len(data)-1], *data.iloc[len(data)-1])
print(board)
player1 = Player(**{"title": "Seamus", "piece": "iron", "position": 10, "money": 1700, "properties": board})
print(player1)
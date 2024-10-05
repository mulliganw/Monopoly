import random
import json
import pandas as pd
from dataclasses import dataclass, asdict
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
        for player in self.properties:
            print(player.dict())
            out.update(player.dict())
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

    def dict(self):

        return asdict(self).items()


@dataclass
class Player:
    title: str
    piece: str
    position: int
    money: int
    properties: List[Property]

    #Converts dataclass to dictionary
    def dict(self):
        return asdict(self)



def read_data(in_filename: str):
    data = pd.read_csv(in_filename, index_col=0)
    properties = []
    for title in data.index.values:
        values = [int(x) for x in data.loc[title].iloc[0: -1]]
        properties.append(Property(title, *values, data.loc[title].iloc[-1]))
    return properties

tiles = read_data("properties.csv")
game = Game(Player("Seamus", "dog", 10, 1500, tiles))
game.to_json()



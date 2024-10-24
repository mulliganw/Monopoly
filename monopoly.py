import random
import json
from time import sleep

import pandas as pd
from dataclasses import dataclass, asdict
from typing import List
import pickle


class Game:
    def __init__(self, players):
        self.grid = []
        self.players: List[Player] = players
        self.turn: int = 0
        self.properties: List[Property] = []

    def roll(self, player_id):
        roll = random.randint(1, 6) + random.randint(1, 6)
        self.players[player_id].position += roll
        self.players[player_id].position %= 22

    def buy(self, player_id, property_id):
        if self.players[player_id].money >= self.properties[property_id].price:
            self.players[player_id].properties.append(self.properties[property_id])
            self.players[player_id].money -= self.properties[property_id].price

    def to_json(self):
        out = {
            "turn": self.turn
        }
        for player in self.properties:
            out.update(player.dict())
        with open("sample.json", "w") as outfile:
            json.dump(out, outfile)


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
    id: int
    title: str
    piece: str
    position: int
    money: int
    properties: List[Property]

    # Converts dataclass to dictionary
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
player1 = Player(0, "Seamus", "dog", 0, 1500, [])
player2 = Player(1, "Nickolai", "dog", 0, 1500, [])
game = Game([player1, player2])
game.properties = tiles
print(len(tiles))

game.to_json()

while True:
    for i in range(0, 2, 1):
        game.roll(i)
        print(game.players[i].position)
        game.buy(i, game.players[i].position)
        [print(str(game.players[i].properties[j])+"\n") for j in range(len(game.players[i].properties))]
        sleep(5)

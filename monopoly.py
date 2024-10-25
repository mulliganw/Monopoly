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

    def buy(self, player_id):
        player = self.players[player_id]
        property_id = player.position
        property = self.properties[property_id]
        if player.money >= property.price and property.owner==-1:
            player.properties.append(property_id)
            player.money -= self.properties[property_id].price
            property.owner = player_id


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
    id: int
    title: str
    price: int
    # Level is the number of houses/hotels on a property. 0: none, 5: hotel
    level: int
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
    # The owner will be the player id
    owner: int

    def dict(self):
        return asdict(self).items()


@dataclass
class Player:
    id: int
    title: str
    piece: str
    position: int
    money: int
    # The player owns a list of property IDs
    properties: List[int]

    # Converts dataclass to dictionary
    def dict(self):
        return asdict(self)


def read_data(in_filename: str):
    data = pd.read_csv(in_filename, index_col=0)
    properties = []
    for title in data.index.values:
        values = [int(x) for x in data.loc[title].iloc[0: -1]]
        properties.append(Property(title, *values, data.loc[title].iloc[-1], -1))
    return properties


tiles = read_data("properties.csv")
player1 = Player(0, "Seamus", "dog", 0, 1500, [])
player2 = Player(1, "Nickolai", "dog", 0, 1500, [])
game = Game([player1, player2])
game.properties = tiles

game.to_json()

while True:
    for ID in range(0, 2, 1):
        print(game.players[ID].title)
        game.roll(ID)
        print(game.players[ID].position)
        game.buy(ID)
        for property in game.players[ID].properties:
            print(game.properties[property])


        print("\n\n")
        sleep(2)

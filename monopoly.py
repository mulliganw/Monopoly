import random
import json
import numpy as np
import pandas as pd


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


class Player:
    def __init__(self, title, piece):
        self.title = title
        self.piece = piece
        self.position = 0
        self.money = 1500
        self.properties = {}

    def to_json(self):
        return {
            "title": self.title,
            "piece": self.piece,
            "position": self.position,
            "money": self.money,
            "properties": list(self.properties.keys()),
        }


class Property(Tile):
    def __init__(self, title, position, price):
        super().__init__(
            title=title,
            position=position
        )
        self.price = price

    def __str__(self):
        return str(self.title)


"""
Reads property data from csv and lets you index data by column(Type of value like price)
or row (Property name like Board Walk)
"""
data = pd.read_csv("properties.csv", index_col=0)
print(data.index.values[-1])
print(data)
player1 = Player("Seamus", "Hat")
game = Game({player1.title: player1})
boardwalk = Property(str(data.index.values[-1]), 39, int(data.loc[data.index.values[-1]][0]))
game.properties.update({boardwalk.title: boardwalk})
game.roll(player1)
game.buy(player1, boardwalk)
game.to_json()
json_example = {"n": 10}
print(player1.properties)
print(player1.position)
print(player1.money)

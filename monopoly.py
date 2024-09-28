import random


class Game:
    def __init__(self, players):
        self.grid = []
        self.players = players
        self.turn = 0

    def roll(self, player_id: int):
        roll = random.randint(1, 6) + random.randint(1, 6)
        self.players[player_id].position+=roll
        self.players[player_id].position%=40

class Tile:
    def __init__(self, title, position):
        self.title = title
        self.position = position


class Player:
    def __init__(self, name, piece):
        self.name = name
        self.piece = piece
        self.position = 0


class Property(Tile):
    def __init__(self, title, position, price):
        super().__init__(
            title=title,
            position=position
        )
        self.price = price


player1 = Player("Seamus", "Hat")

game = Game([player1])
print(player1.position)


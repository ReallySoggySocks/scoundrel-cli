import random
import sys

SUITS = ["H", "D", "S", "C"]
RANKS = {"1" : 1, "2" : 2, "3" : 3, "4" : 4, "5" : 5 , "6" : 6, "7" : 7, "8" : 8, "9" : 9, "10" : 10, "J" : 11, "Q" : 12, "K" :13, "A" : 14}
PLAYER_HP = 20
DECK_COUNT = 52
ROOM_COUNT = 4


class Player:
    def __init__(self):
        self.hp = PLAYER_HP
        self.damage = None
        self.weapon = None

    def select_card(self, card):
        if card.suit == "H":
            self.hp += card.rank
        elif card.suit == "S" or card.suit == "C":
            self.hp -= card.rank
        elif card.suit == "D":
            card.equip()
            self.damage = card.rank
            self.weapon = f"{card.rank}{card.suit}"

class Card:
    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank
        self.equipped = False

    def discard(self):
        del self

    def equip(self):
        self.equipped = True

class Deck:
    def __init__(self):
        self.count = DECK_COUNT
        self.cards = []

    def start_deck(self):
        for s in SUITS:
            for r in RANKS:
                if (s == "d" or s == "h") and RANKS[r] > 10:
                    self.count -= 1
                    pass

                self.cards.append(Card(s, r))
        random.shuffle(self.cards)
            
    def first_draw(self, room):
        for i in range(ROOM_COUNT):
            room.cards.append(self.cards.pop(i))

    def shuffle(self):
        random.shuffle(self.cards)

    def draw_cards(self, room):
        for i in range(ROOM_COUNT - 1):
            room.card.append(self.cards.pop(i))

class Room:
    def __init__(self, count):
        self.count = count
        self.cards = []

    def in_play(self, player):
        print("-----------------")
        print("Dungeon Room:", end=" ")
        for card in self.cards:
            print(f"{card.rank}{card.suit}", end= " ")
        print("\n-----------------")
        print(f"Player HP: {player.hp}")
        print(f"Current Weapon: {player.weapon}")

    def card_chosen(self, card):
        self.cards.remove(card)
        self.count -= 1
        if card.equipped == False:
            card.discard()


def main():
    player = Player()
    deck = Deck()
    deck.start_deck()
    room = Room(ROOM_COUNT)
    deck.first_draw(room)

    room.in_play(player)


if __name__ == "__main__":
    main()
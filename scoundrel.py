import random
import os

SUITS = ["H", "D", "S", "C"]
RANKS = {"1" : 1, "2" : 2, "3" : 3, "4" : 4, "5" : 5 , "6" : 6, "7" : 7, "8" : 8, "9" : 9, "10" : 10, "J" : 11, "Q" : 12, "K" :13, "A" : 14}
MAX_HP = 20
DECK_COUNT = 52
ROOM_COUNT = 4


class Player:
    def __init__(self):
        self.hp = MAX_HP
        self.damage = None
        self.weapon = None
        self.killed = [None]

    def select_card(self, card):
        card_rank = RANKS[card.rank]

        if card.suit == "H":
            self.hp += card_rank
            if self.hp > MAX_HP:
                self.hp =MAX_HP

        elif card.suit == "S" or card.suit == "C":
            if self.weapon:
                enemy_damage = self.damage - card_rank
                if enemy_damage < 0:
                    enemy_damage = 0

                self.hp -= enemy_damage
                self.killed.append(card)
            else:
                self.hp -= card_rank

        elif card.suit == "D":
            card.equip()
            self.damage = card_rank
            self.weapon = f"{card.rank}{card.suit}"

class Card:
    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank
        self.equipped = False

    def equip(self):
        self.equipped = True

class Deck:
    def __init__(self):
        self.count = DECK_COUNT
        self.cards = []

    def start_deck(self):
        for s in SUITS:
            for r in RANKS:
                if (s == "S" or s == "H") and RANKS[r] > 10:
                    self.count -= 1
                    pass
                else:    
                    self.cards.append(Card(s, r))
        random.shuffle(self.cards)
            
    def first_draw(self, room):
        for i in range(ROOM_COUNT):
            room.cards.append(self.cards.pop(i))

    def shuffle(self):
        random.shuffle(self.cards)

    def draw_cards(self, room):
        room.count = ROOM_COUNT
        for i in range(1, ROOM_COUNT):
            room.cards.append(self.cards.pop(i))

class Room:
    def __init__(self, count):
        self.count = count
        self.cards = []

    def in_play(self, player):
        print("-----------------")
        print("Dungeon Room:", end=" ")
        for card in self.cards:
            print(f"{card.rank}{card.suit}", end= " ")
        print(f"\n\nHP: {player.hp}")
        print(f"Weapon: {player.weapon}")
        if player.killed[-1] is not None:
            print(f"Previous Monster Slain: {player.killed[-1].rank}{player.killed[-1].suit}")
        print("\n-----------------")

    def card_chosen(self, card):
        for c in self.cards:
            if card.rank == c.rank and card.suit == c.suit:
                self.cards.remove(c)
        self.count -= 1


def main():
    player = Player()
    deck = Deck()
    deck.start_deck()
    room = Room(ROOM_COUNT)
    deck.first_draw(room)

    while deck.count > 0:
        if room.count == 1:
            deck.draw_cards(room)

        room.in_play(player)
        player_input = input("Choose a Card: ")

        if len(player_input) > 2:
            player_rank = player_input[0] + player_input[1]
            player_suit = player_input[2]
        else:
            player_rank = player_input[0]
            player_suit = player_input[1]

        chosen_card = Card(player_suit.capitalize(), player_rank.capitalize())

        player.select_card(chosen_card)
        room.card_chosen(chosen_card)

        deck.count -= 1

        os.system("clear")

        if player.hp < 0:
            print("You Lose!")
            break
        elif deck.count == 0:
            print("You Win!")
            break
    quit()


if __name__ == "__main__":
    main()
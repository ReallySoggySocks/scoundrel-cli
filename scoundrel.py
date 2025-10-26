import random
import os
import re

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
                enemy_damage = card_rank - self.damage

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
        self.cards = []
        self.count = DECK_COUNT

    def start_deck(self):
        for s in SUITS:
            for r in RANKS:
                if (s == "D" and RANKS[r] > 10) or (s == "H" and RANKS[r] > 10):
                    self.count -= 1
                    pass
                else:    
                    self.cards.append(Card(s, r))
        random.shuffle(self.cards)
            
    def first_draw(self, room):
        for i in range(ROOM_COUNT):
            room.cards.append(self.cards.pop(i))
            self.count -= 1
        room.count = ROOM_COUNT

    def draw_cards(self, room):
        if self.count > ROOM_COUNT:
            for i in range(1, ROOM_COUNT):
                room.cards.append(self.cards.pop(i))
                self.count -= 1
            room.count = ROOM_COUNT
        else:
            for i in range(1, self.count):
                room.cards.append(self.cards.pop(i))
                self.count -= 1
                room.count += 1

class Room:
    def __init__(self):
        self.cards = []
        self.count = ROOM_COUNT

    def in_play(self, player):
        print("-----------------")
        print("Dungeon Room:", end=" ")
        for card in self.cards:
            print(f"{card.rank}{card.suit}", end= " ")
        print(f"\n\nHP: {player.hp}")
        print(f"Weapon: {player.weapon} |", end=" ")
        if player.killed[-1] is not None:
            print(f"Previous Monster Slain: {player.killed[-1].rank}{player.killed[-1].suit}")
        print("\n-----------------")

    def card_chosen(self, card):
        for c in self.cards:
            if card.rank == c.rank and card.suit == c.suit:
                self.cards.remove(c)
                self.count -= 1

    def player_pass(self, deck):
        random.shuffle(self.cards)
        for i in range(len(self.cards)):
            deck.cards.append(self.cards.pop())
            self.count -= 1


def validate_input(room, inputs, rooms_left):
    while True:
            try:
                player_input = input("Choose a card: ")

                if player_input.capitalize() == "Q" or player_input.capitalize() == "QUIT":
                    quit()
                
                if player_input.capitalize() == "P" or player_input.capitalize() == "PASS":
                    if len(inputs) != 0 and (inputs[-1] == "P" or inputs[-1] == "PASS"):
                        print("Previous turn was already passed")
                        continue

                    if rooms_left <= 1:
                        print("No rooms left to pass")
                        continue

                    else:
                        os.system("clear")
                        inputs.append(player_input.capitalize())
                        print("Previous Turn Passed")
                        return player_input.capitalize()
                

                if len(player_input) == 2  or len(player_input) == 3:
                    pass
                else:
                    print("Invalid Input.")
                    continue
        
                player_rank = re.findall(r"\d", player_input)
                player_suit = re.findall(r"\D", player_input)

                if len(player_suit) != 0:
                    pass
                else:
                    print("No card suit.")
                    continue

                if len(player_rank) == 0:
                    player_rank = str(player_suit[0])
                    player_suit = str(player_suit[1])

                elif len(player_rank) == 2:
                    player_rank = "".join(player_rank)
                    player_suit = str(player_suit[0])

                else:
                    player_rank = player_rank[0]
                    player_suit = str(player_suit[0])

                player_suit = player_suit.capitalize()
                player_rank = player_rank.capitalize()

                if player_suit in SUITS:
                    pass
                else:
                    print("Invalid card suit")
                    continue

                if player_rank in RANKS:
                    pass
                else:
                    print("Invalid card rank")
                    continue
            
                room_suits = []
                room_ranks = []
                for card in room.cards:
                    room_ranks.append(card.rank)
                    room_suits.append(card.suit)
            
                if player_rank in room_ranks and player_suit in room_suits:
                    inputs.append(player_rank + player_suit)
                    return(player_rank, player_suit)
                else:
                    print("Card not in room")
                    continue

            except ValueError:
                print("Invalid Card. Please choose a valid card")

def main():
    player = Player()
    deck = Deck()
    deck.start_deck()
    room = Room()
    deck.first_draw(room)
    os.system("clear")
    player_inputs = [None]
    ROOMS_LEFT = DECK_COUNT // ROOM_COUNT

    while True:
        if len(player_inputs) > 2:
            del player_inputs[0]

        if room.count == 1:
            deck.draw_cards(room)
            ROOMS_LEFT -= 1

        room.in_play(player)

        validated_input = validate_input(room, player_inputs, ROOMS_LEFT)
        
        if validated_input == "P" or validated_input == "PASS":
            room.player_pass(deck)
            deck.first_draw(room)
            room.in_play(player)
            validated_input = validate_input(room, player_inputs, ROOMS_LEFT)

        player_rank = validated_input[0]
        player_suit = validated_input[1]
        
        chosen_card = Card(player_suit, player_rank)

        player.select_card(chosen_card)
        room.card_chosen(chosen_card)

        os.system("clear")

        if player.hp <= 0:
            print("You Lose!")
            break
        elif deck.count <= 1 and room.count == 0:
            print("You Win!")
            break
    quit()


if __name__ == "__main__":
    main()
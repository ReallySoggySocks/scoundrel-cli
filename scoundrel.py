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

    def player_combat(self, card):
        enemy_damage = RANKS[card.rank]

        previous_enemy = self.killed[-1]
        if previous_enemy != None:
            previous_enemy_damage = RANKS[previous_enemy.rank]

        if self.weapon == None:
            self.hp -= enemy_damage

        elif self.weapon != None:
            reduced_damage = enemy_damage - self.damage

            if reduced_damage < 0:
                reduced_damage = 0

            if previous_enemy != None and previous_enemy_damage < enemy_damage:
                try:
                    player_input = input("Do you wish to fight barehanded?(Y/N): ")
                    player_input = player_input.capitalize()

                    if player_input == "Y":
                        self.hp -= enemy_damage
                        self.killed.append(card)
                        return
                        
                    elif player_input == "N":
                        return player_input
                    
                except ValueError:
                    print("Invalid Input. Please type Y or N")
            else:
                self.hp -= reduced_damage
                self.killed.append(card)

    def select_card(self, card):
        card_rank = RANKS[card.rank]

        if card.suit == "H":
            self.hp += card_rank
            if self.hp > MAX_HP:
                self.hp =MAX_HP

        elif card.suit == "S" or card.suit == "C":
            player_combat = self.player_combat(card)
            if player_combat == "N":
                return player_combat
            

        elif card.suit == "D":
            self.killed = [None]
            self.damage = card_rank
            self.weapon = f"{card.rank}{card.suit}"

class Card:
    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank
        self.equipped = False

class Deck:
    def __init__(self):
        self.cards = []
        self.count = DECK_COUNT

    def start_deck(self):
        for s in SUITS:
            for r in RANKS:
                if (s == "D" and RANKS[r] > 10) or (s == "H" and RANKS[r] > 10):
                    pass
                else:    
                    self.cards.append(Card(s, r))
        self.count = len(self.cards)
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
        self.count = 0

def tutorial():
    os.system("clear")
    while True:
        try:
            print("----------\nWelcome to Scoundrel!")
            print("You can type q at any time to exit")
            print("If you wish to skip the tutorial, type s")
            print("----------\n")
            player_input = input("Type y to continue or q to quit: ")
            os.system("clear")
            if player_input.capitalize() == "Q":
                quit()
            elif player_input.capitalize() == "Y":
                pass
            elif player_input.capitalize() == "S":
                return
            else:
                print("Wrong answer!")

            print("----------\nHere's how the cards work:")
            print("\n\nCard suits are represented by their first character. (C = Clubs, S = Spades, H = Hearts, D = Diamonds)")
            print("\n\nSuits are card type:\n-.Clubs(S) and Spades(S) are enemies\n-.Hearts(H) are health potions\n-.Diamonds(D) are weapons")
            print("\nRanks are card strength:\n1-10 = Given Value, J = 11, Q = 12, K = 13, A = 14")
            print("----------\n")
            player_input = input("Make sense? ")
            os.system("clear")
            if player_input.capitalize() == "Y":
                pass
            elif player_input.capitalize() == "Q":
                quit()
            else:
                print("Wrong again!")
                continue
    
            print("----------\nYou have a max hp of 20 and health potions do not over heal.")
            print("(If you have 20 hp and grab a 10H, you stay at 20.)")
            print("You lose the run if your health hits 0 before you clear the dungeon.")
            print("----------\n")
            player_input = input("Got it? ")
            os.system("clear")
            if player_input.capitalize() == "Y":
                pass
            elif player_input.capitalize() == "Q":
                quit()
            else:
                print("Again? Really?")
                continue

            print("----------")
            print("Now lets talk about weapons\n")
            print("Weapons(Diamond cards) reduce the amount of damage you take.")
            print("The damage is your weapon rank - the enemy rank.")
            print("However, they have durability. I'll explain how that works in a second.")
            print("----------\n")
            player_input == input("Ready to get a feel for it? ")
            if player_input.capitalize() == "Y":
                break
            elif player_input.capitalize() == "Q":
                quit()
            else:
                print("Having fun?")

            combat_tutorial()
            break

        except ValueError:
            print("Plese input a valid response.")

    input("All set to start? ")

def combat_tutorial():
    pass

def validate_input(player, room, inputs, rooms_left):
    while True:
            try:
                player_input = input("Choose a card: ")
                player_input = player_input.capitalize()

                if player_input == "Q" or player_input == "QUIT":
                    quit()
                
                elif player_input == "P" or player_input == "PASS":
                    if len(inputs) != 0 and inputs[-1] == "P":
                        print("Previous turn was already passed")
                        continue

                    elif rooms_left <= 1:
                        print("No rooms left to pass")
                        continue

                    else:
                        os.system("clear")
                        inputs.append(player_input)
                        print("Previous Turn Passed")
                        return player_input
                

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
                    chosen_card = Card(player_suit, player_rank)

                    player_selection = player.select_card(chosen_card)

                    if player_selection == "N":
                        print("Please choose another card.")
                        continue
                    
                    inputs.append(chosen_card.rank + chosen_card.suit)

                    return chosen_card
                else:
                    print("Card not in room")
                    continue

            except ValueError:
                print("Invalid Card. Please choose a valid card")

def main():
    tutorial()
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

        validated_input = validate_input(player, room, player_inputs, ROOMS_LEFT)
        
        if validated_input == "P":
            room.player_pass(deck)
            deck.first_draw(room)
            room.in_play(player)
            validated_input = validate_input(player, room, player_inputs, ROOMS_LEFT)

        chosen_card = validated_input
        
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
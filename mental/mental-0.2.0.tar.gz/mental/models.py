import random


class Card:
    def __init__(self, name, id_in_deck):
        self.name = name
        self.id_in_deck = id_in_deck
        self.encryptions = []

    def __str__(self):
        return "({}, {}, {})".format(self.name, self.id_in_deck, self.encryptions)

    def encrypt(self, key):
        self.encryptions.append(key)
        
    def decrypt(self, key):
        self.encryptions.remove(key)

class Deck:
    def __init__(self, cards):
        self.cards = cards

    def shuffle(self):
        random.shuffle(self.cards)
    
    def sequential_enc(self, key_gen):
        [card.encrypt(key_gen(i)) for i, card in enumerate(self)]

    def sequential_dec(self, key_gen):
        [card.decrypt(key_gen(i)) for i, card in enumerate(self)]

    def encrypt(self, key):
        [card.encrypt(key) for card in self]

    def decrypt(self, key):
        [card.decrypt(key) for card in self]

    @staticmethod
    def full_deck():
        card_number = 0
        cards = []
        for suit in ["spades", "clubs", "diamonds", "hearts"]:
            for card in ["ace"] + [str(num) for num in range(2, 10 + 1)] + ["jack", "queen", "king"]:
                cards.append(Card(card + " of " + suit, card_number))
                card_number += 1
        return Deck(cards)

    @staticmethod
    def deck_of_aces():
        cards = []
        card_number = 0
        for suit in ["spades", "clubs", "diamonds", "hearts"]:
                cards.append(Card("ace of " + suit, card_number))
                card_number += 1
        return Deck(cards)

    def __iter__(self):
        return iter(self.cards)

class Player:
    def __init__(self, name, deck):
        self.deck = deck
        self.name = name

    def shuffle(self):
        self.deck.shuffle()

    def encrypt(self, key):
        self.deck.encrypt(key)

    def decrypt(self, key):
        self.deck.decrypt(key)

    def sequential_enc(self, key_gen):
        self.deck.sequential_enc(key_gen)

    def sequential_dec(self, key_gen):
        self.deck.sequential_dec(key_gen)

    def pass_to_player(self, player):
        player.deck = self.deck
        self.deck = None
    
    def __str__(self):
        return_lines = []
        if self.deck:
            return_lines.append("{}'s cards:".format(self.name))
            for card in self.deck:
                return_lines.append(card.__str__())
        else:
            return_lines.append("{} has no cards".format(self.name))
        
        return_lines.append('')
        return '\n'.join(return_lines)

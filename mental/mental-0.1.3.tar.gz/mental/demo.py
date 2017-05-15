from .models import Deck, Player, Card


def test_drive():
    alice, bob = Player("Alice", Deck.deck_of_aces()), Player("Bob", None)
    print(alice)
    print(bob)

    alice.shuffle()

    alice.encrypt(2)
    
    print(alice)
    print(bob)

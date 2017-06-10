from .models import Deck, Player, Card


def test_drive():
    alice, bob = Player("Alice", Deck.deck_of_aces()), Player("Bob", None)

    def status():
        print(alice)
        print(bob)
        print("")

    def say(string):
        print(string)
        print("")

    def trivial_gen(name):
        def generator(num):
            return "{}-{}".format(name, num)
        return generator

    alice_generator = trivial_gen("Alice")
    bob_generator = trivial_gen("Bob")
        

    status()

    say("Alice will shuffle and encrypt the cards")
    alice.shuffle()
    alice.encrypt("Alice's key")
    status()

    say("Alice will pass the cards to Bob")
    alice.pass_to_player(bob)
    status()

    say("Bob will shuffle and encrypt the cards again and hand them back to Alice")
    bob.shuffle()
    bob.encrypt("Bob's key")
    bob.pass_to_player(alice)
    status()

    say("Alice will decrypt her part in the encryption")
    alice.decrypt("Alice's key")
    status()
    
    say("Alice will encrypt each card with a different key and hand the cards to Bob")
    alice.sequential_enc(alice_generator)
    alice.pass_to_player(bob)
    status()

    say("Bob will remove it's first key off and encrypt each card with a separate key")
    bob.decrypt("Bob's key")
    bob.sequential_enc(bob_generator)
    status()

    say("Now if everyone agrees that someone needs to see the first card,\nsay it's about to be dealt to somebody, all the players will reveal \ntheir first sequential key to the player to decrypt the card:")
    
    bob.deck.cards[0].decrypt(alice_generator(0))
    bob.deck.cards[0].decrypt(bob_generator(0))

    status()


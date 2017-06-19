from itertools import product
from ticpy.src.game import main


def test_game(mocker):
    list_of_valid_choices = map(lambda x: str(x[0]) + str(x[1]), list(product([1, 2, 3], ['a', 'b', 'c'])))
    mocker.patch('ticpy.src.game.inp', side_effect=list_of_valid_choices)
    main()

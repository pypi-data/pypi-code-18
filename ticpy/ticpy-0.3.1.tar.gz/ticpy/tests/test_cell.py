from ticpy.src.constants import SEED, SEED_REPR


def test_clear(cell):
    assert cell.content == SEED.EMPTY
    cell.content = SEED.CROSS
    cell.clear()
    assert cell.content == SEED.EMPTY


def test_str(cell):
    cell.content = SEED.CROSS
    assert str(cell) == SEED_REPR[SEED.CROSS]

from GRP_.package_two.pack_two import PackTwo


def test_process():
    p2 = PackTwo()
    assert 2 == p2.process()
    
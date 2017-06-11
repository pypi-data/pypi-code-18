from GRP_sample_app.package_one.pack_one import PackOne


def test_do():
    p1 = PackOne()
    assert 'My name is PackOne' == p1.do()


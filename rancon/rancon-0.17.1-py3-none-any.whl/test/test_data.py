from dotmap import DotMap

TEST_SERVICES = [DotMap({
    'name': sname,
    'host': 'host_{}'.format(sname),
    'port': str(101 + i),
}) for i, sname in enumerate(('1', '2', '3'))]

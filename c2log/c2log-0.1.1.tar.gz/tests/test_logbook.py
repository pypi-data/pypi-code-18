from unittest.mock import mock_open
from unittest.mock import patch

from c2log.logbook import interleave_workouts


def test_interleave_workouts(logbook_header, logbook_workouts):
    def custom_open(*args):
        if args[0] == 'logbook/LogDataAccessTbl.bin':
            content = logbook_header
        elif args[0] == 'logbook/LogDataStorage.bin':
            content = logbook_workouts

        file_obj = mock_open().return_value
        file_obj.read.side_effect = lambda x: content.pop()
        return file_obj

    with patch('builtins.open', new=custom_open):
        w = next(interleave_workouts('logbook'))
        assert len(w) == 64
        assert w[0] == 1
        assert w[32] == 0xa

        w = next(interleave_workouts('logbook'))
        assert len(w) == 64
        assert w[0] == 2
        assert w[32] == 0xb

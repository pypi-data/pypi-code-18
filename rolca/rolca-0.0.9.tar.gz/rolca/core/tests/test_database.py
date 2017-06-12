# pylint: disable=missing-docstring
import unittest
from datetime import datetime, timedelta

from rolca.core.models import Author, Contest, Photo, Theme


class DatabaseTestCase(unittest.TestCase):
    def test_contest_str(self):
        contest = Contest(title="Test contest")
        self.assertEqual(str(contest), "Test contest")

    def test_contest_active(self):
        contest = Contest()
        now = datetime.now()
        day = timedelta(days=1)

        # active contest
        contest.start_date = now - day
        contest.end_date = now + day
        self.assertTrue(contest.is_active())

        # past contest
        contest.start_date = now - 2 * day
        contest.end_date = now - day
        self.assertFalse(contest.is_active())

        # future contest
        contest.start_date = now + day
        contest.end_date = now + 2 * day
        self.assertFalse(contest.is_active())

    def test_theme_str(self):
        theme = Theme(title="Test theme")
        self.assertEqual(str(theme), "Test theme")

    def test_file_str(self):
        # TODO
        pass

    def test_participant_str(self):
        participent = Author(first_name="Janez", last_name="Novak")
        self.assertEqual(str(participent), "Janez Novak")

    def test_photo_str(self):
        photo = Photo(title="Test photo")
        self.assertEqual(str(photo), "Test photo")

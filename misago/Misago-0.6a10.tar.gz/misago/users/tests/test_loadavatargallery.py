from django.core.management import call_command
from django.test import TestCase
from django.utils.six import StringIO

from misago.users.management.commands import loadavatargallery
from misago.users.models import AvatarGallery


class LoadAvatarGalleryTests(TestCase):
    def test_regen_blank_avatar(self):
        """command regens blank avatar"""
        command = loadavatargallery.Command()

        out = StringIO()
        call_command(command, stdout=out)
        command_output = out.getvalue().splitlines()[0].strip()

        self.assertEqual(command_output, "New galleries have been loaded.")

        self.assertTrue(AvatarGallery.objects.exists())

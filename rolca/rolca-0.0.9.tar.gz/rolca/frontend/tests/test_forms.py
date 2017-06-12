# pylint: disable=missing-docstring
from datetime import date
from mock import patch

from django.contrib.auth import get_user_model
from django.db import IntegrityError
from django.test import TestCase, override_settings

from rolca.core.models import Author, Contest, File, Photo, Theme
from rolca.frontend.forms import PhotoForm
from rolca.frontend.tests.utils import get_image_field


class PhotoFormTest(TestCase):
    def setUp(self):
        user_model = get_user_model()
        self.user = user_model.objects.create_user(username='user')

    def tearDown(self):
        for file_ in File.objects.all():
            file_.file.delete()
            file_.thumbnail.delete()

    def test_pass(self):
        today = date.today()
        contest = Contest.objects.create(
            user=self.user, title='Test contest', start_date=today, end_date=today)
        theme = Theme.objects.create(title='Test theme', contest=contest, n_photos=2)
        author = Author.objects.create(user=self.user)

        form = PhotoForm(data={'title': 'My image'}, files={'photo': get_image_field()})
        form.is_valid()  # generate cleaned_data attribute

        form.save(user=self.user, author=author, theme=theme)

        self.assertEqual(File.objects.count(), 1)
        self.assertEqual(Photo.objects.count(), 1)

    @patch('rolca.frontend.forms.Photo')
    def test_transaction(self, photo_patch):
        photo_patch.objects.create.side_effect = IntegrityError

        form = PhotoForm(data={'title': 'My image'}, files={'photo': get_image_field()})
        form.is_valid()  # generate cleaned_data attribute

        with self.assertRaises(IntegrityError):
            form.save(user=self.user, author='', theme='')

        self.assertEqual(File.objects.count(), 0)

    @override_settings(ROLCA_MAX_SIZE=1)
    def test_file_size_validation(self):
        form = PhotoForm(data={'title': 'My image'}, files={'photo': get_image_field()})
        self.assertFalse(form.is_valid())

    @override_settings(ROLCA_MAX_LONG_EDGE=50)
    def test_long_edge_validation(self):
        form = PhotoForm(data={'title': 'My image'}, files={'photo': get_image_field()})
        self.assertFalse(form.is_valid())

    @override_settings(ROLCA_ACCEPTED_FORMATS=['png'])
    def test_file_format_validation(self):
        form = PhotoForm(data={'title': 'My image'}, files={'photo': get_image_field()})
        self.assertFalse(form.is_valid())

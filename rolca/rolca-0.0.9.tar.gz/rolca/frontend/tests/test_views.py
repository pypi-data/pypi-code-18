# pylint: disable=missing-docstring,no-member
import os

from django.contrib.auth import get_user_model
from django.test import Client, TestCase, override_settings
from django.urls import reverse

from rolca.core.models import Author, Contest, File, Photo, Theme

PHOTO_PATH = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'files', 'photo.jpg')


class UploadViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = get_user_model().objects.create(
            username='user',
            first_name='Janez',
            last_name='Novak',
            email='janez.novak@rolca.si',
        )
        cls.contest = Contest.objects.create(
            user=cls.user,
            title='Test contest',
            start_date='2016-01-01',
            end_date='2016-01-31',
        )
        cls.theme_1 = Theme.objects.create(
            user=cls.user,
            title='First theme',
            contest=cls.contest,
            n_photos=2,
        )
        cls.theme_2 = Theme.objects.create(
            user=cls.user,
            title='Second theme',
            contest=cls.contest,
            n_photos=1,
        )

    def setUp(self):
        self.client = Client()
        self.client.session['kwargs'] = {'contest_id': self.contest.pk}
        self.client.session.save()

        self.theme_1_id = str(self.theme_1.pk)
        self.theme_2_id = str(self.theme_2.pk)
        self.management_form_data = {
            self.theme_1_id + '-TOTAL_FORMS': self.theme_1.n_photos,
            self.theme_1_id + '-INITIAL_FORMS': 0,
            self.theme_1_id + '-MAX_NUM_FORMS': self.theme_1.n_photos,
            self.theme_2_id + '-TOTAL_FORMS': self.theme_2.n_photos,
            self.theme_2_id + '-INITIAL_FORMS': 0,
            self.theme_2_id + '-MAX_NUM_FORMS': self.theme_2.n_photos,
        }

        self.upload_url = reverse('rolca-frontend:upload', kwargs={'contest_id': self.contest.pk})

    def tearDown(self):
        for file_ in File.objects.all():
            file_.file.delete()
            file_.thumbnail.delete()

    def test_author_initial_data(self):
        self.client.force_login(self.user)
        resp = self.client.get(self.upload_url)

        self.assertEqual(resp.context['author_form']['first_name'].value(), 'Janez')
        self.assertEqual(resp.context['author_form']['last_name'].value(), 'Novak')
        self.assertEqual(resp.context['author_form']['email'].value(), 'janez.novak@rolca.si')

    def test_author_not_loggedin(self):
        resp = self.client.get(self.upload_url)

        self.assertEqual(resp.context['author_form']['first_name'].value(), None)
        self.assertEqual(resp.context['author_form']['last_name'].value(), None)
        self.assertEqual(resp.context['author_form']['email'].value(), None)
        self.assertEqual(resp.context['author_form']['email'].field.required, True)

    def test_empty_theme_formsets(self):
        resp = self.client.get(self.upload_url)

        formsets = resp.context['theme_formsets']

        self.assertEqual(formsets[0]['theme'], self.theme_1)
        self.assertEqual(len(formsets[0]['formset'].forms), 2)

        self.assertEqual(formsets[1]['theme'], self.theme_2)
        self.assertEqual(len(formsets[1]['formset'].forms), 1)

    def test_no_photo(self):
        data = {
            'author-first_name': 'Janez',
            'author-last_name': 'Novak',
            'author-email': 'janez.novak@rolca.si',
        }
        data.update(self.management_form_data)
        resp = self.client.post(self.upload_url, data)
        self.assertEqual(resp.status_code, 200)

        messages = list(resp.context['messages'])
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), 'Upload at least one photo.')

        self.assertEqual(Author.objects.count(), 0)

    def test_not_loggedin_upload_ok(self):
        with open(PHOTO_PATH, 'rb') as photo_file:
            data = {
                'author-first_name': 'Janez',
                'author-last_name': 'Novak',
                'author-email': 'janez.novak@rolca.si',
                self.theme_1_id + '-0-title': 'Photo 1',
                self.theme_1_id + '-0-photo': photo_file,
            }
            data.update(self.management_form_data)
            resp = self.client.post(self.upload_url, data, follow=True)
        self.assertEqual(resp.status_code, 200)

        self.assertEqual(Author.objects.count(), 1)
        self.assertEqual(Photo.objects.count(), 1)

        author = Author.objects.last()
        self.assertEqual(author.first_name, 'Janez')
        self.assertEqual(author.last_name, 'Novak')
        self.assertEqual(author.email, 'janez.novak@rolca.si')
        self.assertEqual(author.user, None)

        photo = Photo.objects.last()
        self.assertEqual(photo.theme, self.theme_1)
        self.assertEqual(photo.title, 'Photo 1')
        self.assertEqual(photo.author, author)
        self.assertEqual(photo.user, None)

    def test_loggedin_upload_ok(self):
        self.client.force_login(self.user)

        with open(PHOTO_PATH, 'rb') as photo_file:
            data = {
                'author-first_name': 'Janez',
                'author-last_name': 'Novak',
                'author-email': 'janez.novak@rolca.si',
                self.theme_1_id + '-0-title': 'Photo 1',
                self.theme_1_id + '-0-photo': photo_file,
            }
            data.update(self.management_form_data)
            resp = self.client.post(self.upload_url, data, follow=True)
        self.assertEqual(resp.status_code, 200)

        self.assertEqual(Author.objects.count(), 1)
        self.assertEqual(Photo.objects.count(), 1)

        author = Author.objects.last()
        self.assertEqual(author.first_name, 'Janez')
        self.assertEqual(author.last_name, 'Novak')
        self.assertEqual(author.email, 'janez.novak@rolca.si')
        self.assertEqual(author.user, self.user)

        photo = Photo.objects.last()
        self.assertEqual(photo.theme, self.theme_1)
        self.assertEqual(photo.title, 'Photo 1')
        self.assertEqual(photo.author, author)
        self.assertEqual(photo.user, self.user)

    def test_upload_two_photos(self):
        with open(PHOTO_PATH, 'rb') as photo_file_1:
            with open(PHOTO_PATH, 'rb') as photo_file_2:
                data = {
                    'author-first_name': 'Janez',
                    'author-last_name': 'Novak',
                    'author-email': 'janez.novak@rolca.si',
                    self.theme_1_id + '-0-title': 'Photo 1',
                    self.theme_1_id + '-0-photo': photo_file_1,
                    self.theme_2_id + '-0-title': 'Photo 2',
                    self.theme_2_id + '-0-photo': photo_file_2,
                }
                data.update(self.management_form_data)
                resp = self.client.post(self.upload_url, data, follow=True)
        self.assertEqual(resp.status_code, 200)

        self.assertEqual(Author.objects.count(), 1)
        self.assertEqual(Photo.objects.count(), 2)

        author = Author.objects.last()
        self.assertEqual(author.first_name, 'Janez')
        self.assertEqual(author.last_name, 'Novak')
        self.assertEqual(author.email, 'janez.novak@rolca.si')
        self.assertEqual(author.user, None)

        photo = Photo.objects.get(theme=self.theme_1)
        self.assertEqual(photo.title, 'Photo 1')
        self.assertEqual(photo.author, author)
        self.assertEqual(photo.user, None)

        photo = Photo.objects.get(theme=self.theme_2)
        self.assertEqual(photo.title, 'Photo 2')
        self.assertEqual(photo.author, author)
        self.assertEqual(photo.user, None)

    def test_missing_photo(self):
        data = {
            'author-first_name': 'Janez',
            'author-last_name': 'Novak',
            'author-email': 'janez.novak@rolca.si',
            self.theme_1_id + '-0-title': 'Photo 1',
        }
        data.update(self.management_form_data)
        resp = self.client.post(self.upload_url, data, follow=True)
        self.assertEqual(resp.status_code, 200)

        self.assertEqual(Author.objects.count(), 0)
        self.assertEqual(Photo.objects.count(), 0)

        self.assertEqual(
            resp.context['theme_formsets'][0]['formset'].forms[0].errors['photo'].as_text(),
            '* This field is required.'
        )

    def test_missing_title(self):
        with open(PHOTO_PATH, 'rb') as photo_file:
            data = {
                'author-first_name': 'Janez',
                'author-last_name': 'Novak',
                'author-email': 'janez.novak@rolca.si',
                self.theme_1_id + '-0-photo': photo_file,
            }
            data.update(self.management_form_data)
            resp = self.client.post(self.upload_url, data, follow=True)
        self.assertEqual(resp.status_code, 200)

        self.assertEqual(Author.objects.count(), 1)
        self.assertEqual(Photo.objects.count(), 1)

        author = Author.objects.last()
        self.assertEqual(author.first_name, 'Janez')
        self.assertEqual(author.last_name, 'Novak')
        self.assertEqual(author.email, 'janez.novak@rolca.si')
        self.assertEqual(author.user, None)

        photo = Photo.objects.last()
        self.assertEqual(photo.theme, self.theme_1)
        self.assertEqual(photo.title, '')
        self.assertEqual(photo.author, author)
        self.assertEqual(photo.user, None)

    @override_settings(ROLCA_MAX_LONG_EDGE=2)
    def test_long_edge_validation_fail(self):
        with open(PHOTO_PATH, 'rb') as photo_file:
            data = {
                'author-first_name': 'Janez',
                'author-last_name': 'Novak',
                'author-email': 'janez.novak@rolca.si',
                self.theme_1_id + '-0-title': 'Photo 1',
                self.theme_1_id + '-0-photo': photo_file,
            }
            data.update(self.management_form_data)
            resp = self.client.post(self.upload_url, data, follow=True)
        self.assertEqual(resp.status_code, 200)

        self.assertEqual(Author.objects.count(), 0)
        self.assertEqual(Photo.objects.count(), 0)

        self.assertEqual(
            resp.context['theme_formsets'][0]['formset'].forms[0].errors['photo'].as_text(),
            '* Long edge of the image cannot excede 2px.'
        )

    @override_settings(ROLCA_MAX_SIZE=100)
    def test_file_size_validation_fail(self):
        with open(PHOTO_PATH, 'rb') as photo_file:
            data = {
                'author-first_name': 'Janez',
                'author-last_name': 'Novak',
                'author-email': 'janez.novak@rolca.si',
                self.theme_1_id + '-0-title': 'Photo 1',
                self.theme_1_id + '-0-photo': photo_file,
            }
            data.update(self.management_form_data)
            resp = self.client.post(self.upload_url, data, follow=True)
        self.assertEqual(resp.status_code, 200)

        self.assertEqual(Author.objects.count(), 0)
        self.assertEqual(Photo.objects.count(), 0)

        self.assertEqual(
            resp.context['theme_formsets'][0]['formset'].forms[0].errors['photo'].as_text(),
            '* Uploaded file must be smaller than 100 B.'
        )

    @override_settings(ROLCA_ACCEPTED_FORMATS=['PNG'])
    def test_acc_fmt_validation_fail(self):
        with open(PHOTO_PATH, 'rb') as photo_file:
            data = {
                'author-first_name': 'Janez',
                'author-last_name': 'Novak',
                'author-email': 'janez.novak@rolca.si',
                self.theme_1_id + '-0-title': 'Photo 1',
                self.theme_1_id + '-0-photo': photo_file,
            }
            data.update(self.management_form_data)
            resp = self.client.post(self.upload_url, data, follow=True)
        self.assertEqual(resp.status_code, 200)

        self.assertEqual(Author.objects.count(), 0)
        self.assertEqual(Photo.objects.count(), 0)

        self.assertEqual(
            resp.context['theme_formsets'][0]['formset'].forms[0].errors['photo'].as_text(),
            '* Only following image types are supported: PNG'
        )

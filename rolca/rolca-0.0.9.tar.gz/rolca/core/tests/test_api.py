# pylint: disable=missing-docstring
from datetime import date, timedelta

from mock import MagicMock, Mock, patch

from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile

from rest_framework import status
from rest_framework.response import Response
from rest_framework.test import APIRequestFactory, APITestCase, force_authenticate

from rolca.core.api.viewsets import ContestViewSet, PhotoViewSet
from rolca.core.models import Author, Contest, File, Photo, Theme


class ContestApiTest(APITestCase):
    def setUp(self):
        self.factory = APIRequestFactory()

        self.contest_list_view = ContestViewSet.as_view({
            'get': 'list',
            'post': 'create',
        })
        self.contest_detail_view = ContestViewSet.as_view({
            'get': 'retrieve',
            'put': 'update',
            'patch': 'partial_update',
            'delete': 'destroy',
        })

        self.user = MagicMock(spec=get_user_model(), is_superuser=False)
        self.super_user = MagicMock(spec=get_user_model(), is_superuser=True)

    @patch('rolca.core.api.viewsets.ContestViewSet.create')
    def test_create_permissions(self, contest_create_mock):
        contest_create_mock.return_value = MagicMock(spec=Response)
        request = self.factory.post('', {}, format='json')

        # public user
        resp = self.contest_list_view(request)
        self.assertEqual(resp.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(contest_create_mock.call_count, 0)

        # normal user
        force_authenticate(request, self.user)
        resp = self.contest_list_view(request)
        self.assertEqual(resp.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(contest_create_mock.call_count, 0)

        # admin user
        force_authenticate(request, self.super_user)
        resp = self.contest_list_view(request)
        self.assertEqual(contest_create_mock.call_count, 1)

    @patch('rolca.core.api.viewsets.ContestViewSet.list')
    def test_get_list_permissions(self, contest_list_mock):
        contest_list_mock.return_value = MagicMock(spec=Response)
        request = self.factory.get('', format='json')

        # public user
        self.contest_list_view(request)
        self.assertEqual(contest_list_mock.call_count, 1)
        contest_list_mock.reset_mock()

        contest_list_mock.reset_mock()

        # normal user
        force_authenticate(request, self.user)
        self.contest_list_view(request)
        self.assertEqual(contest_list_mock.call_count, 1)

    @patch('rolca.core.api.viewsets.ContestViewSet.retrieve')
    def test_get_detail_permissions(self, contest_retrieve_mock):
        contest_retrieve_mock.return_value = MagicMock(spec=Response)
        request = self.factory.get('', format='json')

        # public user
        self.contest_detail_view(request, pk=1)
        self.assertEqual(contest_retrieve_mock.call_count, 1)

        contest_retrieve_mock.reset_mock()

        # normal user
        force_authenticate(request, self.user)
        self.contest_detail_view(request, pk=1)
        self.assertEqual(contest_retrieve_mock.call_count, 1)

    @patch('rolca.core.api.viewsets.ContestViewSet.update')
    def test_put_permissions(self, contest_update_mock):
        contest_update_mock.return_value = MagicMock(spec=Response)
        request = self.factory.put('', {}, format='json')

        # public user
        resp = self.contest_detail_view(request, pk=1)
        self.assertEqual(resp.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(contest_update_mock.call_count, 0)

        # normal user
        force_authenticate(request, self.user)
        resp = self.contest_detail_view(request, pk=1)
        self.assertEqual(resp.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(contest_update_mock.call_count, 0)

        # admin user
        force_authenticate(request, self.super_user)
        resp = self.contest_detail_view(request, pk=1)
        self.assertEqual(contest_update_mock.call_count, 1)

    @patch('rolca.core.api.viewsets.ContestViewSet.partial_update')
    def test_patch_permissions(self, contest_update_mock):
        contest_update_mock.return_value = MagicMock(spec=Response)
        request = self.factory.patch('', {}, format='json')

        # public user
        resp = self.contest_detail_view(request, pk=1)
        self.assertEqual(resp.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(contest_update_mock.call_count, 0)

        # normal user
        force_authenticate(request, self.user)
        resp = self.contest_detail_view(request, pk=1)
        self.assertEqual(resp.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(contest_update_mock.call_count, 0)

        # admin user
        force_authenticate(request, self.super_user)
        resp = self.contest_detail_view(request, pk=1)
        self.assertEqual(contest_update_mock.call_count, 1)

    @patch('rolca.core.api.viewsets.ContestViewSet.destroy')
    def test_delete_permissions(self, contest_destroy_mock):
        contest_destroy_mock.return_value = MagicMock(spec=Response)
        request = self.factory.delete('', {}, format='json')

        # public user
        resp = self.contest_detail_view(request, pk=1)
        self.assertEqual(resp.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(contest_destroy_mock.call_count, 0)

        # normal user
        force_authenticate(request, self.user)
        resp = self.contest_detail_view(request, pk=1)
        self.assertEqual(resp.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(contest_destroy_mock.call_count, 0)

        # admin user
        force_authenticate(request, self.super_user)
        resp = self.contest_detail_view(request, pk=1)
        self.assertEqual(contest_destroy_mock.call_count, 1)


class PhotoViewSetTest(APITestCase):
    def setUp(self):
        user_model = get_user_model()
        self.creator = user_model.objects.create_user(username='creator')
        self.user1 = user_model.objects.create_user(username='user1')
        self.user2 = user_model.objects.create_user(username='user2')

        today = date.today()
        tomorrow = today + timedelta(days=1)
        self.contest = Contest.objects.create(
            user=self.creator, title='Test contest', start_date=today, end_date=tomorrow)

        theme = Theme.objects.create(title='Test theme', contest=self.contest, n_photos=2)

        author1 = Author.objects.create(user=self.user1)
        author2 = Author.objects.create(user=self.user2)

        file_mock = SimpleUploadedFile('photo.jpg', b'fake photo')

        # pk must be set to skip on-create procedure
        self.file1 = File.objects.create(pk=1, user=self.user1, file=file_mock)
        self.file2 = File.objects.create(pk=2, user=self.user2, file=file_mock)
        self.file3 = File.objects.create(pk=3, user=self.user2, file=file_mock)

        Photo.objects.create(
            title="Photo 1", user=self.user1, author=author1, theme=theme, photo=self.file1)
        Photo.objects.create(
            title="Photo 2", user=self.user2, author=author2, theme=theme, photo=self.file2)
        Photo.objects.create(
            title="Photo 3", user=self.user2, author=author2, theme=theme, photo=self.file3)

    def tearDown(self):
        self.file1.file.delete()
        self.file2.file.delete()
        self.file3.file.delete()

    def test_photo_queryset(self):
        viewset_mock = Mock(spec=PhotoViewSet)

        viewset_mock.request = Mock(user=self.user2)
        self.assertEqual(len(PhotoViewSet.get_queryset(viewset_mock)), 2)

        self.contest.publish_date = date.today() - timedelta(days=1)
        self.contest.save()

        viewset_mock.request = Mock(user=self.user2)
        self.assertEqual(len(PhotoViewSet.get_queryset(viewset_mock)), 3)

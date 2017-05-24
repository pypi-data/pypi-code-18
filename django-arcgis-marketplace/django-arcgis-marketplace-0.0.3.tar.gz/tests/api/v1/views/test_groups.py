import responses

from rest_framework import status

from ...shortcuts import add_response
from ...views import BaseViewTests


class GroupiewTests(BaseViewTests):

    @responses.activate
    def test_group_list_200_OK(self):
        add_response(
            'GET',
            'community/groups',
            body={'total': 1}
        )

        response = self.client.get(
            self.reverse('group-list'), {
                'q': 'group'
            }
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @responses.activate
    def test_group_create_201_CREATED(self):
        add_response(
            'POST',
            'community/createGroup',
            body={'success': True}
        )

        response = self.client.post(
            self.reverse('group-list'), {
                'title': 'my item',
                'access': 'public'
            }
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    @responses.activate
    def test_group_detail_200_OK(self):
        add_response(
            'GET',
            'community/groups/test',
            body={'id': 'test'}
        )

        response = self.client.get(
            self.reverse('group-detail', args=('test',))
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], 'test')

    @responses.activate
    def test_group_update_200_OK(self, method=None):
        add_response(
            'POST',
            'community/groups/test/update',
            body={'title': 'updated'}
        )

        if method is None:
            method = 'put'

        response = getattr(self.client, method)(
            self.reverse('group-detail', args=('test',)), {
                'title': 'updated'
            }
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'updated')

    def test_group_partial_update_200_OK(self):
        self.test_group_update_200_OK('patch')

    @responses.activate
    def test_group_delete_204_NO_CONTENT(self):
        add_response(
            'POST',
            'community/groups/test/delete',
            body={'success': True}
        )

        response = self.client.delete(
            self.reverse('group-detail', args=('test',))
        )

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    @responses.activate
    def test_group_add_200_OK(self, method=None):
        users = 'alice,bob'

        add_response(
            'POST',
            'community/groups/test/addUsers',
            body={'added': users.split(',')}
        )

        response = self.client.post(
            self.reverse('group-add', args=('test',)), {
                'users': users
            }
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @responses.activate
    def test_group_invite_200_OK(self, method=None):
        users = 'alice,bob'

        add_response(
            'POST',
            'community/groups/test/invite',
            body={'success': True}
        )

        response = self.client.post(
            self.reverse('group-invite', args=('test',)), {
                'users': users
            }
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @responses.activate
    def test_group_items_200_OK(self, method=None):
        add_response(
            'GET',
            'content/groups/test',
            body={'total': 1}
        )

        response = self.client.get(
            self.reverse('group-items', args=('test',))
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @responses.activate
    def test_group_config_map_200_OK(self, method=None):
        add_response(
            'POST',
            'community/groups/test/update',
            body={'title': 'updated'}
        )

        response = self.client.post(
            self.reverse('group-config-map', args=('test',))
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

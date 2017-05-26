from ppg_common.clients.base import BaseClient


class PandoraClient(BaseClient):
    urls = {
        'create_box': '/v1/box',
        'box': '/v1/box/{}',
        'files': '/v1/files/{}',
        'files_query': '/v1/files'
    }

    def __init__(self, host, port, ssl=False, session=None):
        super(PandoraClient, self).__init__(host, port, ssl, session)

    def create_box(self, box_name):
        """
        Function for creating box with box_name
        :param box_name: wanted name for new box
        :param x-session: user session id
        :return: box info 
        """
        query_box_url = self.urls.get('create_box')
        return self.post(query_box_url, body={}, query={'name': box_name})

    def list_owned_boxes(self):
        """
        Function for listing all owned boxes
        :param x-session: user session id
        :return: list of boxes
        """
        url = self.urls.get('create_box')
        return self.get(url, query={"shared": 'False'})

    def list_shared_boxes(self):
        """
        Function for listing all shared boxes
        :param x-session: user session id
        :return: list of boxes
        """
        url = self.urls.get('create_box')
        return self.get(url, query={"shared": 'True'})

    def list_box(self, box_id):
        """
        Function for listing all files in box
        :param box_id: box for which files are listed
        :return: list of whiles
        """
        return self.get(self.urls.get("box").format(box_id))

    def delete_box(self, box_id):
        """
        Function for deleting a box
        :param box_id: 
        :param x-session: user session id
        :return: pandora response
        """
        return self.delete(self.urls.get("box").format(box_id))

    def list_by_query(self, box_id, inquiry):
        """
        Function for list by quer
        :param box_id: 
        :param x-session: user session id
        :param inquiry: 
        :return: pandora respnse
        """
        url = self.urls.get("box").format(box_id)
        return self.get(url, query={"inquiry": inquiry})

    def update_by_query(self, box_id, inquiry, tag_name, tag_value):
        url = self.urls.get("box").format(box_id)
        return self.patch(url,
                          query={
                              "inquiry": inquiry, "tag-name": tag_name,
                              "tag-value": tag_value
                          })

    def delete_by_query(self, box_id, inquiry):
        url = self.urls.get("box").format(box_id)
        return self.delete(url, query={"inquiry": inquiry})

    def delete_file(self, file_id):
        """
        Function for deleting file
        :param file_id: id of file to be deleted
        :return: response 
        """
        url = self.urls.get("files").format(file_id)
        return self.delete(url)

    def copy_file(self, file_id, name, box_id):
        url = self.urls.get("files").format(file_id) + "/copy"
        return self.get(url, query={'boxId': box_id, 'name': name})

    def get_info(self, file_id):
        """
        Functiong for getting info on file
        :param file_id: id of wanted file 
        :return: 
        """
        url = self.urls.get("files").format(file_id) + "/info"
        return self.get(url)

    def add_tag(self, file_id, tag_name, tag_value):
        """
        Function for adding tag to file
        :param file_id: 
        :param tag_name: 
        :param tag_value: 
        """
        url = self.urls.get("files").format(file_id) + "/tag"
        return self.post(url, query={
            'tag-name': tag_name,
            'tag-value': tag_value
        })

    def delete_tag(self, file_id, tag_name, tag_value):
        """
        Function for deleting tag from file 
        :param file_id: 
        :param tag_name: 
        :param tag_value: 
        :return: 
        """
        url = self.urls.get("files").format(file_id) + "/tag"
        return self.post(url,
                         query={
                             'tag-name': tag_name,
                             'tag-value': tag_value
                         }
                         )

    def list_owned_files(self):
        """
        Function for listing all of users owned files
        :param x-session: user session id
        :return: list of owned files
        """
        url = self.urls.get('files_query')
        return self.get(url, query={"shared": 'False'})

    def list_shared_files(self):
        """
        Function for listing all of users owned files
        :param x-session: user session id
        :return: list of shared files
        """
        url = self.urls.get('files_query')
        return self.get(url, query={"shared": 'True'})

    def rename_file(self, file_id):
        """
        Function for renaming file
        """
        url = self.urls.get("files").format(file_id) + '/rename'
        return self.patch(url)

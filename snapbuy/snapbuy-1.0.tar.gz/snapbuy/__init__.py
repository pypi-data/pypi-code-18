from snapbuy.client import HttpClient


class SnapBuy(object):
    def __init__(self, api_key, api_url='http://api.snapbuyapp.com'):
        self.http_client = HttpClient(api_key, api_url)

    def create_app(self, app_name):
        """
        Create an application with given name
        :param app_name:
        :return:
        """
        return self.http_client.do_post(path='/applications', data={'name': app_name})

    def delete_app(self, app_id):
        """
        Delete an application with given app_id
        :param app_id:
        :return:
        """

        return self.http_client.do_delete(path='/applications', data={'id': app_id})

    def get_app_detail(self, app_id):
        """
        Get detail information of an application specified by app_id
        :param app_id:
        :return:
        """

        return self.http_client.do_get(path='/applications/' + app_id)

    def get_all_applications(self):
        """
        Get list of all applications created by api_key owner
        :return:
        """

        return self.http_client.do_get(path='/applications')

    def update_app(self, app_id, new_name):
        """
        Update the name of application specified by app_id
        :param app_id:
        :param new_name:
        :return:
        """

        return self.http_client.do_post(path='/applications/update', data={'id': app_id, 'name': new_name})

    def check_image_indexed(self, app_id, image_url):
        """
        Check if an image located at image_url has been indexed within the scope of application
        specified by app_id

        :param app_id:
        :param image_url:
        :return:
        """

        return self.http_client.do_post(path='/images/check', data={'imageURL': image_url, 'appid': app_id})

    def index_image_from_web(self, app_id, image_url, c1=None, c2=None, c3=None, c4=None, c5=None, metadata=None,
                             title=None, description=None, price=None, url=None, currency=None, passive=False):
        """
        Index an image from web, specified by image_url within scope of application app_id

        :param app_id:
        :param image_url:
        :param c1:
        :param c2:
        :param c3:
        :param c4:
        :param c5:
        :param metadata:
        :param title:
        :param description:
        :param price:
        :param url:
        :param currency:
        :param passive:
        :return:
        """

        payload = {
            'appid': app_id,
            'imageURL': image_url,
            'c1': c1,
            'c2': c2,
            'c3': c3,
            'c4': c4,
            'c5': c5,
            'metadata': metadata,
            'title': title,
            'description': description,
            'price': price,
            'url': url,
            'currency': currency,
            'passive': passive
        }

        return self.http_client.do_post(path='/images', data=payload)

    def index_local_image(self, app_id, image_file, c1=None, c2=None, c3=None, c4=None, c5=None, metadata=None,
                          title=None, description=None, price=None, url=None, currency=None, passive=False):
        """
        Index a local image file within scope of application app_id

        :param app_id:
        :param image_file: A file object associated to an image in local file system.
                Ex: image_file = open('clara.jpg', 'r')
        :param c1:
        :param c2:
        :param c3:
        :param c4:
        :param c5:
        :param metadata:
        :param title:
        :param description:
        :param price:
        :param url:
        :param currency:
        :param passive:
        :return:
        """

        payload = {
            'appid': app_id,
            'c1': c1,
            'c2': c2,
            'c3': c3,
            'c4': c4,
            'c5': c5,
            'metadata': metadata,
            'title': title,
            'description': description,
            'price': price,
            'url': url,
            'currency': currency,
            'passive': passive
        }

        return self.http_client.do_post(path='/images', data=payload, files={'image': image_file})

    def delete_image(self, image_id):
        """
        Delete an image specified by image_id

        :param image_id:
        :return:
        """

        return self.http_client.do_delete(path='/images', data={'id': image_id})

    def search_images(self, app_id, page=1, items_per_page=4, title=None, description=None, passive=False, price=None,
                      c1=None, c2=None, c3=None, c4=None, c5=None, image_id=None, color=None, tags=None):
        """
        Search all images matching filters
        :param app_id:
        :param page:
        :param items_per_page:
        :param title:
        :param description:
        :param passive:
        :param price:
        :param c1:
        :param c2:
        :param c3:
        :param c4:
        :param c5:
        :param image_id:
        :param color:
        :param tags:
        :return:
        """

        payload = {
            'appid': app_id,
            'page': page,
            'itemsPerPage': items_per_page,
            'title': title,
            'description': description,
            'passive': passive,
            'price': price,
            'c1': c1,
            'c2': c2,
            'c3': c3,
            'c4': c4,
            'c5': c5,
            'id': image_id,
            'color': color,
            'tags': tags
        }

        return self.http_client.do_post(path='/images/get_images', data=payload)

    def visual_search_image_from_web(self, app_id, image_url, min_price=None, max_price=None, page=1, items_per_page=4,
                                     c1=None, c2=None, c3=None, c4=None, c5=None, similar_color=None, color=None,
                                     tags=None):
        """

        Visual search for image similar to one locating on image_url

        :param app_id:
        :param image_url:
        :param min_price:
        :param max_price:
        :param page:
        :param items_per_page:
        :param c1:
        :param c2:
        :param c3:
        :param c4:
        :param c5:
        :param similar_color:
        :param color:
        :param tags:
        :return:
        """

        payload = {
            'appid': app_id,
            'imageURL': image_url,
            'minPrice': min_price,
            'maxPrice': max_price,
            'page': page,
            'itemsPerPage': items_per_page,
            'c1': c1,
            'c2': c2,
            'c3': c3,
            'c4': c4,
            'c5': c5,
            'similarColor': similar_color,
            'color': color,
            'tags': tags
        }

        return self.http_client.do_post(path='/images/search', data=payload)

    def visual_search_local_image(self, app_id, image_file, min_price=None, max_price=None, page=1, items_per_page=4,
                                  c1=None, c2=None, c3=None, c4=None, c5=None, similar_color=None, color=None,
                                  tags=None):
        """

        Visual search for image similar to the image image_file from local file system

        :param app_id:
        :param image_file:
        :param min_price:
        :param max_price:
        :param page:
        :param items_per_page:
        :param c1:
        :param c2:
        :param c3:
        :param c4:
        :param c5:
        :param similar_color:
        :param color:
        :param tags:
        :return:
        """

        payload = {
            'appid': app_id,
            'minPrice': min_price,
            'maxPrice': max_price,
            'page': page,
            'itemsPerPage': items_per_page,
            'c1': c1,
            'c2': c2,
            'c3': c3,
            'c4': c4,
            'c5': c5,
            'similarColor': similar_color,
            'color': color,
            'tags': tags
        }

        return self.http_client.do_post(path='/images/search', data=payload, files={'image': image_file})

    def adult_filtering_image_from_web(self, image_url):
        """
        Check if image locating at image_url has adult content or not

        :param image_url:
        :return:
        """

        return self.http_client.do_post(path='/adult_filtering', data={'imageURL': image_url})

    def adult_filtering_local_image(self, image_file):
        """
        Check if image image_file from local file system has adult content or not

        :param image_file:
        :return:
        """

        return self.http_client.do_post(path='/adult_filtering', files={'image': image_file})

    def get_tags_image_from_web(self, image_url):
        """
        Get labels of image locating at image_url

        :param image_url:
        :return:
        """

        return self.http_client.do_post(path='/images/get_labels', data={'imageURL': image_url})

    def get_tags_local_image(self, image_file):
        """
        Get labels of image image_file from local file system

        :param image_file:
        :return:
        """

        return self.http_client.do_post(path='/images/get_labels', files={'image': image_file})

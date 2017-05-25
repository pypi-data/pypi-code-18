#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# @author acrazing - joking.young@gmail.com
# @version 1.0.0
# @since 2017-05-26 00:10:35
#
# Post.py
#
from soulapi.Api import Module


class Post(Module):
    def recommended(self, first_page=1, first_post_id=None, page_index=1, page_size=20, top_post_id=0, _type=10007):
        data = self.api.json(url='/post/recommended', params={
            'firstPage': first_page,
            'firstPostId': first_post_id,
            'pageIndex': page_index,
            'pageSize': page_size,
            'topPostId': top_post_id,
            'type': _type,
            'platform': self.api.platform,
        })
        result = data.get('data', [])
        if len(data) == 0:
            data['next'] = None
        else:
            data['next'] = {
                'first_page': first_page + 1,
                'first_post_id': result[-1]['id'],
                'page_index': page_index + 1,
                'page_size': page_size,
                'top_post_id': result[0]['id'] if result[0]['top'] is True else top_post_id,
                '_type': _type,
            }
        return data

    def like(self, post_id):
        return self.api.json(url='/post/%s/like' % post_id, method='post')

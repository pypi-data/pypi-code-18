"""KnowledgeOwl"""
from __future__ import print_function
import logging
import hammock
from multidimensional_urlencode import urlencode
import simplejson
import json

# We define the possible keys we can use to update/create an article/category
# If keys that are present in the response but should not be updated are updated
#   manually then the article/category starts throwing 500 errors.
ARTICLE_KEYS = ('application_screens', 'article_link', 'author', 'auto_save',
                'callout', 'callout_expire', 'callout_video', 'category',
                'category_view', 'content_article', 'current_version',
                'current_version_id', 'current_version_number', 'date_created',
                'date_deleted', 'date_modified', 'date_published',
                'hide_from_toc', 'index', 'inherited_roles', 'internal_title',
                'languages', 'meta_data', 'meta_description', 'meta_page_title',
                'modified_author', 'name', 'parents', 'pdf',
                'prevent_searching', 'project_id', 'reader_roles',
                'ready_versions', 'redirect_link', 'related_articles',
                'remove_comments', 'remove_feedback', 'remove_pdf',
                'searchTitle', 'search_phrases', 'status', 'summary', 'tags',
                'template_article', 'toc_title', 'url_hash', 'user_teams',
                'view_count', 'visibility')
CATEGORY_KEYS = ('application_screens', 'articles_per_page', 'blog_order',
                 'cat_toggle_override', 'category_link', 'date_created',
                 'date_modified', 'date_published', 'description',
                 'faqChildren', 'faqContent', 'faq_display', 'hide_from_toc',
                 'index', 'inherited_roles', 'languages', 'meta_data',
                 'meta_description', 'meta_page_title', 'name', 'parent_id',
                 'parents', 'project_id', 'reader_roles', 'redirect_link',
                 'related_articles', 'status', 'toc_hide_children', 'toc_title',
                 'type', 'url_hash', 'user_teams', 'visibility')
COMMENT_KEYS = ('article_id', 'author_id', 'content', 'date_created',
                'project_id', 'public_email', 'public_name', 'status',
                'user_submitted')
FILE_KEYS = ('chunk_size', 'contentType', 'date_created', 'date_modified',
             'length', 'md5', 'name', 'project_id', 'status',
             'url')
TAG_KEYS = ('name', 'project_id', 'status')
READER_KEYS = ('agent', 'custom1', 'custom2', 'custom3', 'custom4', 'custom5',
               'date_created', 'date_lastlogin', 'date_modified', 'first_name',
               'icon', 'last_name', 'password', 'pending_projects', 'projects',
               'reader_roles', 'ssoid', 'status', 'username')
ARTICLEVERSION_KEYS = ('article_id', 'auto_save', 'current_version',
                       'date_created', 'date_deleted', 'date_modified',
                       'date_published', 'languages', 'modified_author', 'name',
                       'project_id', 'ready', 'status', 'version_number',
                       'version_reader_roles')
READERROLES_KEYS = ('index', 'name')
SUGGEST_KEYS = ('application_screens', 'auto_save', 'callout', 'callout_expire',
                'callout_video', 'category', 'category_view', 'content_article',
                'current_version', 'current_version_id',
                'current_version_number', 'date_created', 'date_deleted',
                'date_modified', 'date_published', 'hide_from_toc', 'index',
                'inherited_roles', 'languages', 'modified_author', 'name',
                'parents', 'prevent_searching', 'reader_roles', 'remove_pdf',
                'results', 'status', 'toc_title', 'type', 'url_hash',
                'view_count', 'visibility')

# objects = ['article', 'category', 'comment', 'file', 'tag', 'reader',
#            'articleversion', 'readerroles', 'suggest']
# for o in objects:
#     r = ko.knowledgeowl(o).GET(params={'_method': 'explain'}).json()
#     fields = tuple(sorted([str(f['fieldname']) for f in r['data']['fields']]))
#     print(o)
#     print(fields)


class MissingRequiredArg(Exception):
    """Exception for missing required argument."""
    def __init__(self, message):
        super(MissingRequiredArg, self).__init__(message)
        self.message = message
    def __repr__(self):
        print('Missing required argument: {0}'.format(self.message))

class InvalidArg(Exception):
    """Exception for argument that should not be there."""
    def __init__(self, message):
        super(InvalidArg, self).__init__(message)
        self.message = message
    def __repr__(self):
        print('Invalid argument: {0}'.format(self.message))


class KnowledgeOwl(object):
    """KnowledgeOwl interface."""
    def __init__(self, api_key, project_id, version='head'):
        url_string = 'https://app.knowledgeowl.com/api/{0}'.format(version)
        self.knowledgeowl = hammock.Hammock(url_string, auth=(api_key, 'X'), headers={'Content-Type': 'application/json'})
        self.project_id = project_id


    def __call(self, hammock_obj, method, **kwargs):
        resp = getattr(hammock_obj, method.upper())(**kwargs)
        if resp:
            try:
                return resp.json()
            except simplejson.scanner.JSONDecodeError as error:
                logging.critical(error)
                logging.critical('%s Endpoint %s, Args: %s, Error: %s',method, hammock_obj, kwargs, resp.text)
                logging.critical(resp.text)
                raise
        else:
            logging.critical('%s %s %s, Args: %s, Error: %s',method, hammock_obj, resp.status_code, kwargs, resp.text)
            if resp.status_code != 400:
                quit(1)


    def create_article(self, **kwargs):
        """Create KnowledgeOwl Article."""
        for key in ['name', 'visibility', 'status', 'url_hash']:
            if key not in kwargs.keys():
                raise MissingRequiredArg(key)
        for key in kwargs:
            if key not in ARTICLE_KEYS:
                raise InvalidArg(key)
        kwargs['project_id'] = self.project_id
        logging.debug('POST data for create_article: %s', kwargs)
        return self.__call(self.knowledgeowl.article, 'POST', data=json.dumps(kwargs))

    def list_articles(self, **kwargs):
        """List all articles."""
        m_keys = list(ARTICLE_KEYS)
        m_keys.extend(['sort', 'limit'])
        for key in kwargs:
            if key not in m_keys:
                raise InvalidArg(key)

        return self.__call(self.knowledgeowl.article, 'GET', params=urlencode(kwargs))

    def get_article(self, article_id, **kwargs):
        """Retrieve article and it's current version html."""
        for key in kwargs:
            if key not in ['replaceSnippets', '_fields']:
                raise InvalidArg(key)
        return self.__call(self.knowledgeowl.article(article_id), 'GET',
                           data=json.dumps({'_fields': 'current_version'}),
                           params=urlencode(kwargs))

    def update_article(self, article_id, **kwargs):
        """Update article attributes.

        See knowledgeowl.ARTICLE_KEYS for all possible update values.
        """
        for key in kwargs:
            if key not in ARTICLE_KEYS:
                raise InvalidArg(key)
        logging.debug('PUT data for update_article: %s', kwargs)
        return self.__call(self.knowledgeowl.article(article_id), 'PUT',
                           data=json.dumps(kwargs))

    def update_article_content(self, article_id, locale, html, title=None,
                               url_hash=None):
        """Update article content html and optionally title."""
        # If we aren't updating the title we still need to provide it or else it gets set to blank
        if not title:
            title = self.get_article(article_id)['current_version'][locale]['title']
        data = {'current_version': {locale: {'text': html, 'title': title}}}
        if url_hash:
            data['url_hash'] = url_hash
        return self.update_article(article_id, **data)

    def search_articles(self, phrase, **kwargs):
        """Search article matching phrase."""
        for key in kwargs:
            if key not in ['status', '_fields', 'limit']:
                raise InvalidArg(key)
        return self.__call(self.knowledgeowl.suggest, 'GET',
                           data=urlencode({'phrase': phrase}),
                           params=urlencode(kwargs)).json()

    def delete_article(self, article_id):
        """Delete article."""
        return self.update_article(article_id, status='deleted')

    def list_articles_by_category(self, category_id):
        return self.list_articles(category=category_id)

    ############################################################################
    def list_categories(self):
        """List categories."""
        return self.knowledgeowl.category.GET().json()

    def create_category(self, **kwargs):
        """Create KnowledgeOwl Article.

        Required: name, visibility, status, url_hash, type
        Optional: parent_id, toc_title, faq_display, toc_hide_children,
                  description, index, cat_toggle_override, reader_roles,
                  hide_from_toc

        """
        for key in ['name', 'visibility', 'status', 'url_hash', 'type']:
            if key not in kwargs.keys():
                raise MissingRequiredArg(key)
        for key in kwargs:
            if key not in CATEGORY_KEYS:
                raise InvalidArg(key)
        kwargs['project_id'] = self.project_id
        return self.__call(self.knowledgeowl.category, 'POST', data=json.dumps(kwargs))

    def update_category(self, category_id, **kwargs):
        """Update category.

        See knowledgeowl.CATEGORY_KEYS for all possible update values.
        """
        for key in kwargs:
            if key not in CATEGORY_KEYS:
                raise InvalidArg(key)
        return self.__call(self.knowledgeowl.category(category_id), 'PUT', data=json.dumps(kwargs))

    def get_category(self, category_id):
        """Get Category."""
        return self.__call(self.knowledgeowl.category(category_id), 'GET')

    def delete_category(self, category_id):
        """Delete Category."""
        return self.update_category(category_id, status='deleted')

    ############################################################################
    def get_comment(self, comment_id, **kwargs):
        for key in kwargs:
            if key not in ['_fields']:
                raise InvalidArg(key)
        kwargs['project_id'] = self.project_id
        return self.__call(self.knowledgeowl.comment(comment_id), 'GET', params=urlencode(kwargs))

    def list_comments(self, **kwargs):
        for key in kwargs:
            if key not in ['article_id', '_fields', 'sort', 'limit']:
                raise InvalidArg(key)
        return self.__call(self.knowledgeowl.comment, 'GET', params=urlencode(kwargs))

    ############################################################################
    def list_readers(self, **kwargs):
        for key in kwargs:
            if key not in READER_KEYS or key not in ['_fields', 'sort', 'limit']:
                raise InvalidArg(key)
        kwargs['project_id'] = self.project_id
        return self.__call(self.knowledgeowl.reader, 'GET', params=kwargs)

    ############################################################################
    def list_readerroles(self, _fields=None, sort=None, limit=None, **params):
        for key in kwargs:
            if key not in READERROLES_KEYS or key not in ['_fields', 'sort', 'limit']:
                raise InvalidArg(key)
        kwargs['project_id'] = self.project_id
        return self.__call(self.knowledgeowl.readerroles, 'GET', params=urlencode(kwargs))

    def get_readerroles(self, role_id, **kwargs):
        for key in kwargs:
            if key not in ['_fields']:
                raise InvalidArg(key)
        kwargs['project_id'] = self.project_id
        return self.__call(self.knowledgeowl.readerroles(role_id), 'GET', params=urlencode(kwargs))

    ############################################################################
    def explain(self, endpoint):
        self.__call(self.knowledgeowl(endpoint), 'GET', params=urlencode({'_method': 'explain'}))

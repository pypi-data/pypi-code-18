# -*- coding: iso-8859-1 -*-
"""
    MoinMoin - PublishPage action

    This action is a selective rename from <page>_DRAFT to <page>

    @copyright: 2002-2004 Michael Reinsch <mr@uue.org>,
                2006-2007 MoinMoin:ThomasWaldmann,
                2007 MoinMoin:ReimarBauer,
                2017 Conrad Leonard
    @license: GNU GPL, see COPYING for details.
"""
import os
import re
import shutil
from MoinMoin import wikiutil, user
from MoinMoin.Page import Page
from MoinMoin.PageEditor import PageEditor
from MoinMoin.action import ActionBase

class PublishPage(ActionBase):
    """ Publish page action

    Note: the action name is the class name
    """
    def __init__(self, pagename, request):
        ActionBase.__init__(self, pagename, request)
        self.use_ticket = True
        _ = self._
        self.form_trigger = 'publish'
        self.form_trigger_label = _('Publish Page')
        self.newpagename = re.sub('_DRAFT$', '', self.pagename)
        self.publisher_agent = user.User(
                self.request,
                name=self.request.cfg.publisher_agent_user,
                password=self.request.cfg.publisher_agent_pwd)
        assert self.publisher_agent.valid == 1, "publisher_agent_user credentials invalid"

    def is_allowed(self):
        return (
            self.pagename.endswith('_DRAFT') and
            self.request.user.name in self.request.groups.get('PublisherGroup'))

    def check_condition(self):
        _ = self._
        if not self.page.exists():
            return _('This page is already deleted or was never created!')
        else:
            return None

    def do_action(self):
        """ Publish this page to "pagename" """
        _ = self._
        form = self.form
        comment = form.get('comment', u'')
        comment = wikiutil.clean_input(comment)

        # temporarily escalate user privilege
        cfg = self.request.cfg
        original_user = self.request.user
        self.request.user = self.publisher_agent

        draft_text = self.page.get_raw_body()
        draft_text += '''\n----\nCategorySOP\n'''
        newpage = PageEditor(self.request, self.newpagename)
        dummy, rev, exists = newpage.get_rev()
        draft_attachdir = self.page.getPagePath("attachments", check_create=1)
        published_attachdir = newpage.getPagePath("attachments", check_create=1)
        try:
            success, msg = True, newpage.saveText(draft_text, rev, comment=comment)
            # low-level copy of attachments
            shutil.rmtree(published_attachdir, ignore_errors=True)
            shutil.copytree(draft_attachdir, published_attachdir)
        except Exception as e:
            success, msg = False, e.message

        self.request.user = original_user

        return success, msg

    def do_action_finish(self, success):
        if success:
            url = Page(self.request, self.newpagename).url(self.request)
            self.request.http_redirect(url, code=301)
        else:
            self.render_msg(self.make_form(), "dialog")

    def get_form_html(self, buttons_html):
        _ = self._

        options_html = ""

        d = {
            'querytext': _('Really publish this page?'),
            'pagename': wikiutil.escape(self.pagename, True),
            'comment_label': _("Comment"),
            'buttons_html': buttons_html,
            'options_html': options_html,
            }

        return '''
<strong>%(querytext)s</strong>
<br>
<br>
%(options_html)s
<table>
    <tr>
        <td class="label"><label>%(comment_label)s</label></td>
        <td class="content">
            <input type="text" name="comment" size="80" maxlength="200" required>
        </td>
    </tr>
    <tr>
        <td></td>
        <td class="buttons">
            %(buttons_html)s
        </td>
    </tr>
</table>
''' % d

def execute(pagename, request):
    """ Glue code for actions """
    PublishPage(pagename, request).render()


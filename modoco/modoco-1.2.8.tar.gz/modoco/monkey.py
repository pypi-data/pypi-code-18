'''
Odds and ends for monkey-patching
'''

def startContent(self, content_id='content', newline=True, **kw):
    """
    Based on MoinMoin.formatter.text_html.Formatter, customized to apply
    custom id attribute value when page is draft.
    """
    if hasattr(self, 'page'):
        self.request.uid_generator.begin(self.page.page_name)

    result = []
    # Use the content language
    attr = self._langAttr(self.request.content_lang)
    # For custom styling of draft pages
    if hasattr(self, 'page') and self.page.page_name.endswith('_DRAFT'):
        attr['id'] = 'draft-not-sop'
    else:
        attr['id'] = content_id
    result.append(self._open('div', newline=False, attr=attr,
                                allowed_attrs=['align'], **kw))
    result.append(self.anchordef('top'))
    if newline:
        result.append('\n')
    return ''.join(result)

def login_hint(self, request):
    """
    Based on MoinMoin.auth.MoinAuth.login_hint, customized to remove link to
    new account creation
    """
    _ = request.getText
    sendmypasswordlink = request.page.url(request, querystr={'action': 'recoverpass'})

    return _('<a href="%(sendmypasswordlink)s">Forgot your password?</a>') % {
            'sendmypasswordlink': sendmypasswordlink} 

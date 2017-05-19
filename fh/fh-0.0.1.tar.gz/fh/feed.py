from string import Template
from itertools import count
from email import encoders
from email.message import Message
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.utils import format_datetime
from time import mktime
from datetime import datetime
from feedparser import parse
from requests import get

def fetch(url, already_saved):
    t = Template(url)

    url0 = t.safe_substitute(page=0)
    url1 = t.safe_substitute(page=1)

    entries = []

    r = parse(url0)
    entries.extend(r.entries)
    if url0 == url1:
        pass
    else:
        for page in count(1):
            r = parse(t.safe_substitute(page=page))
            if r.entries:
                entries.extend(r.entries)
            else:
                break

    for e in r.entries:
        if not e.link in already_saved:
            m = entry(e)
            if 'author' in r and not m['From']:
                m['From'] = r.author
            yield m

def entry(x):
    m = MIMEMultipart()
    if x.author:
        m['From'] = x.author
    m['X-Feed-Link'] = x.link
    if x.title:
        m['Subject'] = x.title
    else:
        m['Subject'] = x.link
    m['Date'] = published(x.published_parsed)

    if 'summary_detail' in x:
        m.attach(content(x.summary_detail))
    for content_detail in x.get('content', []):
        m.attach(content(content_detail))
    for y in x.links:
        attachment = link(y.href)
        if attachment:
            m.attach(attachment)
    return m

def content(content_detail):
    maintype, subtype = content_detail['type'].split('/', 1)
    return MIMEText(content_detail['value'], subtype)

def link(url):
    r = get(url)
    if r:
        maintype, subtype = r.headers['Content-Type'].split('/', 1)
        if maintype == 'text':
            m = MIMEText(r.text, _subtype=subtype)
        else:
            m = MIMEBase(maintype, subtype)
            m.set_payload(r.content)
            encoders.encode_base64(m)
        m.add_header('Content-Disposition', 'attachment')
        return m

def published(x):
    return format_datetime(datetime.fromtimestamp(mktime(x)))

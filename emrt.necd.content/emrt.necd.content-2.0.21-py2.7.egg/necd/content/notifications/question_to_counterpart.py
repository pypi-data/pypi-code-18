from Acquisition import aq_parent
from emrt.necd.content.question import IQuestion
from five import grok
from Products.CMFCore.interfaces import IActionSucceededEvent
from Products.Five.browser.pagetemplatefile import PageTemplateFile
from utils import notify
from emrt.necd.content.constants import ROLE_CP
from emrt.necd.content.constants import ROLE_LR


@grok.subscribe(IQuestion, IActionSucceededEvent)
def notification_cp(context, event):
    """
    To:     CounterParts
    When:   New draft question to comment on
    """
    _temp = PageTemplateFile('question_to_counterpart.pt')

    if event.action in ['request-for-counterpart-comments']:
        observation = aq_parent(context)
        subject = u'New draft question to comment'
        notify(
            observation,
            _temp,
            subject,
            role=ROLE_CP,
            notification_name='question_to_counterpart'
        )


@grok.subscribe(IQuestion, IActionSucceededEvent)
def notification_lr(context, event):
    """
    To:     LeadReviewer
    When:   New draft question to comment on
    """
    _temp = PageTemplateFile('question_to_counterpart.pt')

    if event.action in ['request-for-counterpart-comments']:
        observation = aq_parent(context)
        subject = u'New draft question to comment'
        notify(
            observation,
            _temp,
            subject,
            role=ROLE_LR,
            notification_name='question_to_counterpart'
        )

from copy import copy
from AccessControl import getSecurityManager
from Acquisition import aq_base
from Acquisition import aq_inner
from Acquisition import aq_parent
from Acquisition.interfaces import IAcquirer
from collective.z3cform.datagridfield import DataGridFieldFactory
from collective.z3cform.datagridfield import DictRow
from emrt.necd.content import MessageFactory as _
from emrt.necd.content.observation import hidden
from five import grok
from plone import api
from plone.app.dexterity.behaviors.discussion import IAllowDiscussion
from plone.dexterity.interfaces import IDexterityFTI
from plone.directives import dexterity
from plone.directives import form
from plone.namedfile.interfaces import IImageScaleTraversable
from time import time
from types import IntType
from types import ListType
from types import TupleType
from types import FloatType
from z3c.form import field
from z3c.form.browser.checkbox import CheckBoxFieldWidget
from zope import schema
from zope.browsermenu.menu import getMenu
from zope.browserpage.viewpagetemplatefile import (
    ViewPageTemplateFile as Z3ViewPageTemplateFile
)
from zope.component import createObject
from zope.component import getUtility
from zope.globalrequest import getRequest
from zope.interface import Invalid
from zope.schema.interfaces import IVocabularyFactory
from zope.lifecycleevent import ObjectModifiedEvent
from zope.event import notify
from z3c.form import interfaces


DEFAULTCONCLUSIONTEXT = u"""For category x and pollutants a, b, c for year[s]... the TERT noted that...
In response to a question raised during the review, [the Member State] explained that... [the Member State provided [a] revised estimate[s] for year[s] [and stated that it will be included in the next submission.]]
The TERT [disagreed][agreed][party agreed] with the [explanation] [revised estimate] provided by [the Member State].
[The TERT decided to calculate a technical correction.][The TERT noted that the issue is below the threshold of significance for technical correction.]
The TERT recommends that... [[the Member State] include the revised estimate in its next submission.]
"""


class ITableRowSchema(form.Schema):

    line_title = schema.TextLine(title=_(u'Title'), required=True)
    co2 = schema.Float(title=_(u'CO\u2082'), required=False)
    ch4 = schema.Float(title=_(u'CH\u2084'), required=False)
    n2o = schema.Float(title=_(u'N\u2082O'), required=False)
    nox = schema.Float(title=_(u'NO\u2093'), required=False)
    co = schema.Float(title=_(u'CO'), required=False)
    nmvoc = schema.Float(title=_(u'NMVOC'), required=False)
    so2 = schema.Float(title=_(u'SO\u2082'), required=False)


class IConclusions(form.Schema, IImageScaleTraversable):
    """
    Conclusions of the Second Phase of the Review
    """

    closing_reason = schema.Choice(
        title=_(u'Conclusion'),
        vocabulary='emrt.necd.content.conclusion_reasons',
        required=True,
    )

    text = schema.Text(
        title=_(u'Text'),
        required=True,
        default=DEFAULTCONCLUSIONTEXT,
    )

    form.widget(ghg_estimations=DataGridFieldFactory)
    ghg_estimations = schema.List(
        title=_(u'GHG estimates [Gg CO2 eq.]'),
        value_type=DictRow(title=u"tablerow", schema=ITableRowSchema),
        default=[
            {'line_title': 'Original estimate', 'co2': 0, 'ch4': 0, 'n2o': 0, 'nox': 0, 'co': 0, 'nmvoc': 0, 'so2': 0},
            {'line_title': 'Technical correction proposed by  TERT', 'co2': 0, 'ch4': 0, 'n2o': 0, 'nox': 0, 'co': 0, 'nmvoc': 0, 'so2': 0},
            {'line_title': 'Revised estimate by MS', 'co2': 0, 'ch4': 0, 'n2o': 0, 'nox': 0, 'co': 0, 'nmvoc': 0, 'so2': 0},
            {'line_title': 'Corrected estimate', 'co2': 0, 'ch4': 0, 'n2o': 0, 'nox': 0, 'co': 0, 'nmvoc': 0, 'so2': 0},

        ],
    )


@form.validator(field=IConclusions['ghg_estimations'])
def check_ghg_estimations(value):
    for item in value:
        for val in item.values():
            if type(val) is FloatType and val < 0:
                raise Invalid(u'Estimation values must be positive numbers')


# Custom content-type class; objects created for this content type will
# be instances of this class. Use this class to add content-type specific
# methods and properties. Put methods that are mainly useful for rendering
# in separate view classes.
class Conclusions(dexterity.Container):
    grok.implements(IConclusions)

    def reason_value(self):
        return self._vocabulary_value(
            'emrt.necd.content.conclusion_reasons',
            self.closing_reason
        )

    def _vocabulary_value(self, vocabulary, term):
        vocab_factory = getUtility(IVocabularyFactory, name=vocabulary)
        vocabulary = vocab_factory(self)
        if not term:
            return u''
        try:
            value = vocabulary.getTerm(term)
            return value.title
        except LookupError:
            return term

    def can_edit(self):
        sm = getSecurityManager()
        return sm.checkPermission('Modify portal content', self)

    def can_delete(self):
        sm = getSecurityManager()
        return sm.checkPermission('Delete objects', self)

    def can_add_files(self):
        sm = getSecurityManager()
        return sm.checkPermission('emrt.necd.content: Add NECDFile', self)

    def get_actions(self):
        parent = aq_parent(self)
        request = getRequest()
        question_menu_items = getMenu(
            'plone_contentmenu_workflow',
            self,
            request
        )
        observation_menu_items = getMenu(
            'plone_contentmenu_workflow',
            parent,
            request
        )
        menu_items = question_menu_items + observation_menu_items
        return [mitem for mitem in menu_items if not hidden(mitem)]

    def get_files(self):
        items = self.values()
        mtool = api.portal.get_tool('portal_membership')
        return [item for item in items if mtool.checkPermission('View', item)]


class AddForm(dexterity.AddForm):
    grok.name('emrt.necd.content.conclusions')
    grok.context(IConclusions)
    grok.require('emrt.necd.content.AddConclusions')

    label = 'Conclusions'
    description = ''

    def updateFields(self):
        super(AddForm, self).updateFields()
        from .observation import IObservation
        conclusion_fields = field.Fields(IConclusions).select(
            'closing_reason', 'text')
        observation_fields = field.Fields(IObservation).select('highlight')
        self.fields = field.Fields(conclusion_fields, observation_fields)
        self.fields['highlight'].widgetFactory = CheckBoxFieldWidget
        self.groups = [g for g in self.groups if g.label == 'label_schema_default']

    def updateWidgets(self):
        super(AddForm, self).updateWidgets()
        self.widgets['text'].rows = 15

        widget_highlight = self.widgets['highlight']
        widget_highlight.template = Z3ViewPageTemplateFile(
            'templates/widget_highlight.pt'
        )

    def update(self):
        super(AddForm, self).update()

        # grab highlight value from observation
        widget_highlight = self.widgets['highlight']
        def set_checked(item):
            updated_item = copy(item)
            updated_item['checked'] = (
                updated_item['value'] in (self.context.highlight or [])
            )
            return updated_item

        widget_highlight.items = map(set_checked, widget_highlight.items)

    def create(self, data={}):
        fti = getUtility(IDexterityFTI, name=self.portal_type)
        container = aq_inner(self.context)
        content = createObject(fti.factory)
        if hasattr(content, '_setPortalTypeName'):
            content._setPortalTypeName(fti.getId())

        # Acquisition wrap temporarily to satisfy things like vocabularies
        # depending on tools
        if IAcquirer.providedBy(content):
            content = content.__of__(container)
        id = str(int(time()))
        content.title = id
        content.id = id
        content.text = self.request.form.get('form.widgets.text', '')
        reason = self.request.form.get('form.widgets.closing_reason', '')
        content.closing_reason = reason[0]
        adapted = IAllowDiscussion(content)
        adapted.allow_discussion = True

        # Update highlight on parent observation
        highlight = self.request.form.get('form.widgets.highlight')
        container.highlight = highlight
        notify(ObjectModifiedEvent(container))

        # Update Observation state
        api.content.transition(
            obj=container,
            transition='draft-conclusions'
        )

        return aq_base(content)

    def updateActions(self):
        super(AddForm, self).updateActions()
        for k in self.actions.keys():
            self.actions[k].addClass('standardButton')


class ConclusionsView(grok.View):
    grok.context(IConclusions)
    grok.require('zope2.View')
    grok.name('view')

    def render(self):
        context = aq_inner(self.context)
        parent = aq_parent(context)
        url = '%s#tab-conclusions' % parent.absolute_url()

        return self.request.response.redirect(url)


class EditForm(dexterity.EditForm):
    grok.name('edit')
    grok.context(IConclusions)
    grok.require('cmf.ModifyPortalContent')

    label = 'Conclusions'
    description = ''
    ignoreContext = False

    def getContent(self):
        context = aq_inner(self.context)
        container = aq_parent(context)
        data = {}
        data['text'] = DEFAULTCONCLUSIONTEXT
        if context.text:
            data['text'] = context.text
        if type(context.closing_reason) in (ListType, TupleType):
            data['closing_reason'] = context.closing_reason[0]
        else:
            data['closing_reason'] = context.closing_reason
        #data['ghg_estimations'] = context.ghg_estimations
        data['highlight'] = container.highlight
        return data

    def updateFields(self):
        super(EditForm, self).updateFields()
        from .observation import IObservation
        conclusion_fields = field.Fields(IConclusions).select(
            'closing_reason', 'text')
        observation_fields = field.Fields(IObservation).select('highlight')
        self.fields = field.Fields(conclusion_fields, observation_fields)
        self.fields['highlight'].widgetFactory = CheckBoxFieldWidget
        self.fields['text'].rows = 15
        self.groups = [g for g in self.groups if g.label == 'label_schema_default']

    def updateWidgets(self):
        super(EditForm, self).updateWidgets()
        self.widgets['text'].rows = 15
        self.widgets['highlight'].template = Z3ViewPageTemplateFile(
            'templates/widget_highlight.pt'
        )

    def updateActions(self):
        super(EditForm, self).updateActions()
        for k in self.actions.keys():
            self.actions[k].addClass('standardButton')

    def applyChanges(self, data):
        super(EditForm, self).applyChanges(data)
        context = aq_inner(self.context)
        container = aq_parent(context)
        text = self.request.form.get('form.widgets.text')
        closing_reason = self.request.form.get('form.widgets.closing_reason')
        context.text = text
        if type(closing_reason) in (ListType, TupleType):
            context.closing_reason = closing_reason[0]
        #context.ghg_estimations = data['ghg_estimations']
        highlight = self.request.form.get('form.widgets.highlight')
        container.highlight = highlight
        notify(ObjectModifiedEvent(context))
        notify(ObjectModifiedEvent(container))

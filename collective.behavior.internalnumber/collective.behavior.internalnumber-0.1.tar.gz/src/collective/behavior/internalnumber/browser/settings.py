# -*- coding: utf-8 -*-

from zope import schema
from zope.component import getAllUtilitiesRegisteredFor, getUtility
from zope.i18n.interfaces import ITranslationDomain
from zope.interface import Interface, implements
from zope.schema.interfaces import IVocabularyFactory
from zope.schema.vocabulary import SimpleVocabulary, SimpleTerm
from z3c.form import form

from plone import api
from plone.app.registry.browser.controlpanel import RegistryEditForm
from plone.app.registry.browser.controlpanel import ControlPanelFormWrapper
from plone.autoform.directives import widget
from plone.dexterity.interfaces import IDexterityFTI
from plone.z3cform import layout

from collective.z3cform.datagridfield import DataGridFieldFactory
from collective.z3cform.datagridfield.registry import DictRow

from .. import _, TYPE_CONFIG


class IPortalTypeConfigSchema(Interface):
    portal_type = schema.Choice(
        title=_("Portal type"),
        vocabulary=u'collective.internalnumber.portaltypevocabulary',
        required=True)
    uniqueness = schema.Bool(
        title=_("Uniqueness"),
        required=False)
    default_number = schema.Int(
        title=_(u'Number of next content item'),
        description=_(u"This value can be used as 'number' variable in tal expression"),
        default=1)
    default_expression = schema.TextLine(
        title=_("Default value tal expression"),
        description=_("Elements 'number', 'member', 'context' and 'portal' are available."),
        default=u"number",
        required=False)


class IInternalNumberConfig(Interface):
    """
    Configuration of internalnumber
    """

    portal_type_config = schema.List(
        title=_(u'By type configuration'),
        value_type=DictRow(title=_("Portal type conf"),
                           schema=IPortalTypeConfigSchema))

    widget('portal_type_config', DataGridFieldFactory)


class SettingsEditForm(RegistryEditForm):
    """
    Define form logic
    """
    form.extends(RegistryEditForm)
    schema = IInternalNumberConfig
    label = _("Internal number behavior configuration")

SettingsView = layout.wrap_form(SettingsEditForm, ControlPanelFormWrapper)


def get_settings():
    ptc = api.portal.get_registry_record(TYPE_CONFIG)
    settings = {}
    if ptc is None:
        return settings
    for row in ptc:
        expr = row['default_expression'] and row['default_expression'] or u''
        settings[row['portal_type']] = {'u': row['uniqueness'], 'nb': row['default_number'], 'expr': expr}
    return settings


def get_pt_settings(pt):
    settings = get_settings()
    if pt in settings:
        return settings[pt]
    elif 'glo_bal' in settings:
        return settings['glo_bal']
    return {}


class DxPortalTypesVocabulary(object):
    """ Active mail types vocabulary """
    implements(IVocabularyFactory)

    def __call__(self, context):
        terms = [SimpleTerm('glo_bal', 'glo_bal', _(u'Global configuration'))]
        ftis = getAllUtilitiesRegisteredFor(IDexterityFTI)
        for fti in ftis:
            translation_domain = getUtility(ITranslationDomain, fti.i18n_domain)
            terms.append(SimpleTerm(fti.id, fti.id, translation_domain.translate(fti.title,
                                                                                 context=api.portal.get().REQUEST)))
        return SimpleVocabulary(terms)

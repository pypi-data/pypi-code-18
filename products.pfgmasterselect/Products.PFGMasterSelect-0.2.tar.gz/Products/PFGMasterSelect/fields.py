from Products.ATContentTypes.content import schemata
from Products.Archetypes import atapi
from Products.CMFCore.Expression import Expression
from Products.CMFCore.permissions import View
from Products.DataGridField import DataGridField
from Products.DataGridField import DataGridWidget
from Products.DataGridField import SelectColumn
from Products.MasterSelectWidget.MasterMultiSelectWidget import MasterMultiSelectWidget
from Products.MasterSelectWidget.MasterSelectWidget import MasterSelectWidget
from Products.PloneFormGen.content.fieldsBase import BaseFormField, BaseFieldSchemaStringDefault, vocabularyField, \
    vocabularyOverrideField, LinesVocabularyField, StringVocabularyField
from zope.interface import implements
from .interfaces import IFormMasterSelectStringField, IFormMasterMultiSelectStringField
from Products.PFGMasterSelect.config import PROJECTNAME


class FormMasterSelectFieldMixin:

    def setSlave_fields(self, slave_fields):
        self.Schema()['slave_fields'].set(self, slave_fields)

        def compile_methods(field):
            field = field.copy()
            if 'toggle_method' in field:
                toggle_method = field['toggle_method']
                field['toggle_method'] = Expression('python:' + toggle_method) if toggle_method else None
            if 'vocab_method' in field:
                vocab_method = field['vocab_method']
                field['vocab_method'] = Expression('python:' + vocab_method) if vocab_method else None
            return field

        self.fgField.widget.slave_fields = [compile_methods(field)
                                            for field in slave_fields
                                            if field.get('toggle_method')
                                            or field.get('vocab_method')
                                            or field.get('hide_values')]

    def getActionVocab(self):
        return atapi.DisplayList((
            ('hide', 'Hide'),
            ('show', 'Show'),
            ('enable', 'Enable'),
            ('disable', 'Disable'),
            ('value', 'Value'),
            ('vocabulary', 'Vocabulary'),
        ))

    def getNameVocab(self):
        folder = self.aq_parent
        fieldNames = [field.getName() for field in folder.fgFields()]
        return atapi.DisplayList(zip(fieldNames, fieldNames))


FormMasterSelectFieldSchema = BaseFieldSchemaStringDefault.copy() + atapi.Schema((
    vocabularyField,
    vocabularyOverrideField,
    DataGridField('slave_fields',
                  allow_insert=True,
                  allow_delete=True,
                  allow_reorder=True,
                  columns=('name', 'action', 'vocab_method', 'toggle_method', 'hide_values'),
                  validators=('isColumnFilled', 'isSlaveConfigValid',),
                  widget=DataGridWidget(label='Slave Fields',
                                        description='Configure actions applied on other fields of the Form Folder '
                                                    'when changing this fields state. vocab_method and toggle_method '
                                                    'expect python expressions evaluating to a boolean. The new value '
                                                    'of this field is available as "value" of type string in '
                                                    'vocab_method and toggle_method.',
                                        columns={
                                              'name': SelectColumn('Name', 'getNameVocab'),
                                              'action': SelectColumn('Action', 'getActionVocab'),
                                        }),
                  ),
))

schemata.finalizeATCTSchema(FormMasterSelectFieldSchema, moveDiscussion=False)


class FormMasterSelectStringField(BaseFormField, FormMasterSelectFieldMixin):

    implements(IFormMasterSelectStringField)

    meta_type = "FormMasterSelectStringField"
    schema = FormMasterSelectFieldSchema

    def __init__(self, oid, **kwargs):
        BaseFormField.__init__(self, oid, **kwargs)

        self.fgField = StringVocabularyField('fg_masterselect',
                                             searchable=False,
                                             required=False,
                                             vocabulary=None,
                                             write_permission=View,
                                             widget=MasterSelectWidget(slave_fields=[]))


FormMasterMultiSelectFieldSchema = BaseFieldSchemaStringDefault.copy() + atapi.Schema((
    vocabularyField,
    vocabularyOverrideField,
    DataGridField('slave_fields',
                  allow_insert=True,
                  allow_delete=True,
                  allow_reorder=True,
                  columns=('name', 'action', 'vocab_method', 'toggle_method', 'hide_values'),
                  validators=('isColumnFilled', 'isSlaveConfigValid',),
                  widget=DataGridWidget(label='Slave Fields',
                                        description='Configure actions applied on other fields of the Form Folder '
                                                    'when changing this fields state. vocab_method and toggle_method '
                                                    'expect python expressions evaluating to a boolean. The selected '
                                                    'values of this field are available as "values" of type list of '
                                                    'strings in vocab_method and toggle_method.',
                                        columns={
                                         'name': SelectColumn('Name', 'getNameVocab'),
                                         'action': SelectColumn('Action', 'getActionVocab'),
                                        }),
                  ),
))

schemata.finalizeATCTSchema(FormMasterMultiSelectFieldSchema, moveDiscussion=False)


class FormMasterMultiSelectStringField(BaseFormField, FormMasterSelectFieldMixin):

    implements(IFormMasterMultiSelectStringField)

    meta_type = "FormMasterMultiSelectStringField"
    schema = FormMasterMultiSelectFieldSchema

    def __init__(self, oid, **kwargs):
        BaseFormField.__init__(self, oid, **kwargs)

        self.fgField = LinesVocabularyField('fg_masterselect',
                                            searchable=False,
                                            required=False,
                                            vocabulary=None,
                                            multiValued=True,
                                            write_permission=View,
                                            widget=MasterMultiSelectWidget(slave_fields=[]))


atapi.registerType(FormMasterSelectStringField, PROJECTNAME)
atapi.registerType(FormMasterMultiSelectStringField, PROJECTNAME)

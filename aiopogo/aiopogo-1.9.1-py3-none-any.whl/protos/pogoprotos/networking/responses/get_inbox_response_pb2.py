# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: pogoprotos/networking/responses/get_inbox_response.proto

import sys
_b=sys.version_info[0]<3 and (lambda x:x) or (lambda x:x.encode('latin1'))
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
from google.protobuf import descriptor_pb2
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor.FileDescriptor(
  name='pogoprotos/networking/responses/get_inbox_response.proto',
  package='pogoprotos.networking.responses',
  syntax='proto3',
  serialized_pb=_b('\n8pogoprotos/networking/responses/get_inbox_response.proto\x12\x1fpogoprotos.networking.responses\"\x90\x07\n\x10GetInboxResponse\x12H\n\x06result\x18\x01 \x01(\x0e\x32\x38.pogoprotos.networking.responses.GetInboxResponse.Result\x12L\n\x05inbox\x18\x02 \x01(\x0b\x32=.pogoprotos.networking.responses.GetInboxResponse.ClientInbox\x1a\xb4\x05\n\x0b\x43lientInbox\x12\x61\n\rnotifications\x18\x01 \x03(\x0b\x32J.pogoprotos.networking.responses.GetInboxResponse.ClientInbox.Notification\x12i\n\x11\x62uiltin_variables\x18\x02 \x03(\x0b\x32N.pogoprotos.networking.responses.GetInboxResponse.ClientInbox.TemplateVariable\x1a\xec\x02\n\x0cNotification\x12\x17\n\x0fnotification_id\x18\x01 \x01(\t\x12\x11\n\ttitle_key\x18\x02 \x01(\t\x12\x10\n\x08\x63\x61tegory\x18\x03 \x01(\t\x12\x1b\n\x13\x63reate_timestamp_ms\x18\x04 \x01(\x03\x12\x61\n\tvariables\x18\x05 \x03(\x0b\x32N.pogoprotos.networking.responses.GetInboxResponse.ClientInbox.TemplateVariable\x12`\n\x06labels\x18\x06 \x03(\x0e\x32P.pogoprotos.networking.responses.GetInboxResponse.ClientInbox.Notification.Label\"<\n\x05Label\x12\x0f\n\x0bUNSET_LABEL\x10\x00\x12\n\n\x06UNREAD\x10\x01\x12\x07\n\x03NEW\x10\x02\x12\r\n\tIMMEDIATE\x10\x03\x1ah\n\x10TemplateVariable\x12\x0c\n\x04name\x18\x01 \x01(\t\x12\x0f\n\x07literal\x18\x02 \x01(\t\x12\x0b\n\x03key\x18\x03 \x01(\t\x12\x14\n\x0clookup_table\x18\x04 \x01(\t\x12\x12\n\nbyte_value\x18\x05 \x01(\x0c\"-\n\x06Result\x12\t\n\x05UNSET\x10\x00\x12\x0b\n\x07SUCCESS\x10\x01\x12\x0b\n\x07\x46\x41ILURE\x10\x02\x62\x06proto3')
)



_GETINBOXRESPONSE_CLIENTINBOX_NOTIFICATION_LABEL = _descriptor.EnumDescriptor(
  name='Label',
  full_name='pogoprotos.networking.responses.GetInboxResponse.ClientInbox.Notification.Label',
  filename=None,
  file=DESCRIPTOR,
  values=[
    _descriptor.EnumValueDescriptor(
      name='UNSET_LABEL', index=0, number=0,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='UNREAD', index=1, number=1,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='NEW', index=2, number=2,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='IMMEDIATE', index=3, number=3,
      options=None,
      type=None),
  ],
  containing_type=None,
  options=None,
  serialized_start=793,
  serialized_end=853,
)
_sym_db.RegisterEnumDescriptor(_GETINBOXRESPONSE_CLIENTINBOX_NOTIFICATION_LABEL)

_GETINBOXRESPONSE_RESULT = _descriptor.EnumDescriptor(
  name='Result',
  full_name='pogoprotos.networking.responses.GetInboxResponse.Result',
  filename=None,
  file=DESCRIPTOR,
  values=[
    _descriptor.EnumValueDescriptor(
      name='UNSET', index=0, number=0,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='SUCCESS', index=1, number=1,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='FAILURE', index=2, number=2,
      options=None,
      type=None),
  ],
  containing_type=None,
  options=None,
  serialized_start=961,
  serialized_end=1006,
)
_sym_db.RegisterEnumDescriptor(_GETINBOXRESPONSE_RESULT)


_GETINBOXRESPONSE_CLIENTINBOX_NOTIFICATION = _descriptor.Descriptor(
  name='Notification',
  full_name='pogoprotos.networking.responses.GetInboxResponse.ClientInbox.Notification',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='notification_id', full_name='pogoprotos.networking.responses.GetInboxResponse.ClientInbox.Notification.notification_id', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='title_key', full_name='pogoprotos.networking.responses.GetInboxResponse.ClientInbox.Notification.title_key', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='category', full_name='pogoprotos.networking.responses.GetInboxResponse.ClientInbox.Notification.category', index=2,
      number=3, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='create_timestamp_ms', full_name='pogoprotos.networking.responses.GetInboxResponse.ClientInbox.Notification.create_timestamp_ms', index=3,
      number=4, type=3, cpp_type=2, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='variables', full_name='pogoprotos.networking.responses.GetInboxResponse.ClientInbox.Notification.variables', index=4,
      number=5, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='labels', full_name='pogoprotos.networking.responses.GetInboxResponse.ClientInbox.Notification.labels', index=5,
      number=6, type=14, cpp_type=8, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
    _GETINBOXRESPONSE_CLIENTINBOX_NOTIFICATION_LABEL,
  ],
  options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=489,
  serialized_end=853,
)

_GETINBOXRESPONSE_CLIENTINBOX_TEMPLATEVARIABLE = _descriptor.Descriptor(
  name='TemplateVariable',
  full_name='pogoprotos.networking.responses.GetInboxResponse.ClientInbox.TemplateVariable',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='name', full_name='pogoprotos.networking.responses.GetInboxResponse.ClientInbox.TemplateVariable.name', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='literal', full_name='pogoprotos.networking.responses.GetInboxResponse.ClientInbox.TemplateVariable.literal', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='key', full_name='pogoprotos.networking.responses.GetInboxResponse.ClientInbox.TemplateVariable.key', index=2,
      number=3, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='lookup_table', full_name='pogoprotos.networking.responses.GetInboxResponse.ClientInbox.TemplateVariable.lookup_table', index=3,
      number=4, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='byte_value', full_name='pogoprotos.networking.responses.GetInboxResponse.ClientInbox.TemplateVariable.byte_value', index=4,
      number=5, type=12, cpp_type=9, label=1,
      has_default_value=False, default_value=_b(""),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=855,
  serialized_end=959,
)

_GETINBOXRESPONSE_CLIENTINBOX = _descriptor.Descriptor(
  name='ClientInbox',
  full_name='pogoprotos.networking.responses.GetInboxResponse.ClientInbox',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='notifications', full_name='pogoprotos.networking.responses.GetInboxResponse.ClientInbox.notifications', index=0,
      number=1, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='builtin_variables', full_name='pogoprotos.networking.responses.GetInboxResponse.ClientInbox.builtin_variables', index=1,
      number=2, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[_GETINBOXRESPONSE_CLIENTINBOX_NOTIFICATION, _GETINBOXRESPONSE_CLIENTINBOX_TEMPLATEVARIABLE, ],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=267,
  serialized_end=959,
)

_GETINBOXRESPONSE = _descriptor.Descriptor(
  name='GetInboxResponse',
  full_name='pogoprotos.networking.responses.GetInboxResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='result', full_name='pogoprotos.networking.responses.GetInboxResponse.result', index=0,
      number=1, type=14, cpp_type=8, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='inbox', full_name='pogoprotos.networking.responses.GetInboxResponse.inbox', index=1,
      number=2, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[_GETINBOXRESPONSE_CLIENTINBOX, ],
  enum_types=[
    _GETINBOXRESPONSE_RESULT,
  ],
  options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=94,
  serialized_end=1006,
)

_GETINBOXRESPONSE_CLIENTINBOX_NOTIFICATION.fields_by_name['variables'].message_type = _GETINBOXRESPONSE_CLIENTINBOX_TEMPLATEVARIABLE
_GETINBOXRESPONSE_CLIENTINBOX_NOTIFICATION.fields_by_name['labels'].enum_type = _GETINBOXRESPONSE_CLIENTINBOX_NOTIFICATION_LABEL
_GETINBOXRESPONSE_CLIENTINBOX_NOTIFICATION.containing_type = _GETINBOXRESPONSE_CLIENTINBOX
_GETINBOXRESPONSE_CLIENTINBOX_NOTIFICATION_LABEL.containing_type = _GETINBOXRESPONSE_CLIENTINBOX_NOTIFICATION
_GETINBOXRESPONSE_CLIENTINBOX_TEMPLATEVARIABLE.containing_type = _GETINBOXRESPONSE_CLIENTINBOX
_GETINBOXRESPONSE_CLIENTINBOX.fields_by_name['notifications'].message_type = _GETINBOXRESPONSE_CLIENTINBOX_NOTIFICATION
_GETINBOXRESPONSE_CLIENTINBOX.fields_by_name['builtin_variables'].message_type = _GETINBOXRESPONSE_CLIENTINBOX_TEMPLATEVARIABLE
_GETINBOXRESPONSE_CLIENTINBOX.containing_type = _GETINBOXRESPONSE
_GETINBOXRESPONSE.fields_by_name['result'].enum_type = _GETINBOXRESPONSE_RESULT
_GETINBOXRESPONSE.fields_by_name['inbox'].message_type = _GETINBOXRESPONSE_CLIENTINBOX
_GETINBOXRESPONSE_RESULT.containing_type = _GETINBOXRESPONSE
DESCRIPTOR.message_types_by_name['GetInboxResponse'] = _GETINBOXRESPONSE
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

GetInboxResponse = _reflection.GeneratedProtocolMessageType('GetInboxResponse', (_message.Message,), dict(

  ClientInbox = _reflection.GeneratedProtocolMessageType('ClientInbox', (_message.Message,), dict(

    Notification = _reflection.GeneratedProtocolMessageType('Notification', (_message.Message,), dict(
      DESCRIPTOR = _GETINBOXRESPONSE_CLIENTINBOX_NOTIFICATION,
      __module__ = 'pogoprotos.networking.responses.get_inbox_response_pb2'
      # @@protoc_insertion_point(class_scope:pogoprotos.networking.responses.GetInboxResponse.ClientInbox.Notification)
      ))
    ,

    TemplateVariable = _reflection.GeneratedProtocolMessageType('TemplateVariable', (_message.Message,), dict(
      DESCRIPTOR = _GETINBOXRESPONSE_CLIENTINBOX_TEMPLATEVARIABLE,
      __module__ = 'pogoprotos.networking.responses.get_inbox_response_pb2'
      # @@protoc_insertion_point(class_scope:pogoprotos.networking.responses.GetInboxResponse.ClientInbox.TemplateVariable)
      ))
    ,
    DESCRIPTOR = _GETINBOXRESPONSE_CLIENTINBOX,
    __module__ = 'pogoprotos.networking.responses.get_inbox_response_pb2'
    # @@protoc_insertion_point(class_scope:pogoprotos.networking.responses.GetInboxResponse.ClientInbox)
    ))
  ,
  DESCRIPTOR = _GETINBOXRESPONSE,
  __module__ = 'pogoprotos.networking.responses.get_inbox_response_pb2'
  # @@protoc_insertion_point(class_scope:pogoprotos.networking.responses.GetInboxResponse)
  ))
_sym_db.RegisterMessage(GetInboxResponse)
_sym_db.RegisterMessage(GetInboxResponse.ClientInbox)
_sym_db.RegisterMessage(GetInboxResponse.ClientInbox.Notification)
_sym_db.RegisterMessage(GetInboxResponse.ClientInbox.TemplateVariable)


# @@protoc_insertion_point(module_scope)

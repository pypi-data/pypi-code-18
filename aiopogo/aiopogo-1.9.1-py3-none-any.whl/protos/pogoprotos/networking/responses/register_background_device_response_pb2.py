# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: pogoprotos/networking/responses/register_background_device_response.proto

import sys
_b=sys.version_info[0]<3 and (lambda x:x) or (lambda x:x.encode('latin1'))
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
from google.protobuf import descriptor_pb2
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from pogoprotos.data import background_token_pb2 as pogoprotos_dot_data_dot_background__token__pb2


DESCRIPTOR = _descriptor.FileDescriptor(
  name='pogoprotos/networking/responses/register_background_device_response.proto',
  package='pogoprotos.networking.responses',
  syntax='proto3',
  serialized_pb=_b('\nIpogoprotos/networking/responses/register_background_device_response.proto\x12\x1fpogoprotos.networking.responses\x1a&pogoprotos/data/background_token.proto\"\xda\x01\n RegisterBackgroundDeviceResponse\x12X\n\x06status\x18\x01 \x01(\x0e\x32H.pogoprotos.networking.responses.RegisterBackgroundDeviceResponse.Status\x12/\n\x05token\x18\x02 \x01(\x0b\x32 .pogoprotos.data.BackgroundToken\"+\n\x06Status\x12\t\n\x05UNSET\x10\x00\x12\x0b\n\x07SUCCESS\x10\x01\x12\t\n\x05\x45RROR\x10\x02\x62\x06proto3')
  ,
  dependencies=[pogoprotos_dot_data_dot_background__token__pb2.DESCRIPTOR,])



_REGISTERBACKGROUNDDEVICERESPONSE_STATUS = _descriptor.EnumDescriptor(
  name='Status',
  full_name='pogoprotos.networking.responses.RegisterBackgroundDeviceResponse.Status',
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
      name='ERROR', index=2, number=2,
      options=None,
      type=None),
  ],
  containing_type=None,
  options=None,
  serialized_start=326,
  serialized_end=369,
)
_sym_db.RegisterEnumDescriptor(_REGISTERBACKGROUNDDEVICERESPONSE_STATUS)


_REGISTERBACKGROUNDDEVICERESPONSE = _descriptor.Descriptor(
  name='RegisterBackgroundDeviceResponse',
  full_name='pogoprotos.networking.responses.RegisterBackgroundDeviceResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='status', full_name='pogoprotos.networking.responses.RegisterBackgroundDeviceResponse.status', index=0,
      number=1, type=14, cpp_type=8, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='token', full_name='pogoprotos.networking.responses.RegisterBackgroundDeviceResponse.token', index=1,
      number=2, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
    _REGISTERBACKGROUNDDEVICERESPONSE_STATUS,
  ],
  options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=151,
  serialized_end=369,
)

_REGISTERBACKGROUNDDEVICERESPONSE.fields_by_name['status'].enum_type = _REGISTERBACKGROUNDDEVICERESPONSE_STATUS
_REGISTERBACKGROUNDDEVICERESPONSE.fields_by_name['token'].message_type = pogoprotos_dot_data_dot_background__token__pb2._BACKGROUNDTOKEN
_REGISTERBACKGROUNDDEVICERESPONSE_STATUS.containing_type = _REGISTERBACKGROUNDDEVICERESPONSE
DESCRIPTOR.message_types_by_name['RegisterBackgroundDeviceResponse'] = _REGISTERBACKGROUNDDEVICERESPONSE
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

RegisterBackgroundDeviceResponse = _reflection.GeneratedProtocolMessageType('RegisterBackgroundDeviceResponse', (_message.Message,), dict(
  DESCRIPTOR = _REGISTERBACKGROUNDDEVICERESPONSE,
  __module__ = 'pogoprotos.networking.responses.register_background_device_response_pb2'
  # @@protoc_insertion_point(class_scope:pogoprotos.networking.responses.RegisterBackgroundDeviceResponse)
  ))
_sym_db.RegisterMessage(RegisterBackgroundDeviceResponse)


# @@protoc_insertion_point(module_scope)

# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: pogoprotos/networking/responses/get_gym_details_response.proto

import sys
_b=sys.version_info[0]<3 and (lambda x:x) or (lambda x:x.encode('latin1'))
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
from google.protobuf import descriptor_pb2
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from pogoprotos.data.gym import gym_state_pb2 as pogoprotos_dot_data_dot_gym_dot_gym__state__pb2


DESCRIPTOR = _descriptor.FileDescriptor(
  name='pogoprotos/networking/responses/get_gym_details_response.proto',
  package='pogoprotos.networking.responses',
  syntax='proto3',
  serialized_pb=_b('\n>pogoprotos/networking/responses/get_gym_details_response.proto\x12\x1fpogoprotos.networking.responses\x1a#pogoprotos/data/gym/gym_state.proto\"\x9a\x02\n\x15GetGymDetailsResponse\x12\x30\n\tgym_state\x18\x01 \x01(\x0b\x32\x1d.pogoprotos.data.gym.GymState\x12\x0c\n\x04name\x18\x02 \x01(\t\x12\x0c\n\x04urls\x18\x03 \x03(\t\x12M\n\x06result\x18\x04 \x01(\x0e\x32=.pogoprotos.networking.responses.GetGymDetailsResponse.Result\x12\x13\n\x0b\x64\x65scription\x18\x05 \x01(\t\x12\x15\n\rsecondary_url\x18\x06 \x03(\t\"8\n\x06Result\x12\t\n\x05UNSET\x10\x00\x12\x0b\n\x07SUCCESS\x10\x01\x12\x16\n\x12\x45RROR_NOT_IN_RANGE\x10\x02\x62\x06proto3')
  ,
  dependencies=[pogoprotos_dot_data_dot_gym_dot_gym__state__pb2.DESCRIPTOR,])



_GETGYMDETAILSRESPONSE_RESULT = _descriptor.EnumDescriptor(
  name='Result',
  full_name='pogoprotos.networking.responses.GetGymDetailsResponse.Result',
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
      name='ERROR_NOT_IN_RANGE', index=2, number=2,
      options=None,
      type=None),
  ],
  containing_type=None,
  options=None,
  serialized_start=363,
  serialized_end=419,
)
_sym_db.RegisterEnumDescriptor(_GETGYMDETAILSRESPONSE_RESULT)


_GETGYMDETAILSRESPONSE = _descriptor.Descriptor(
  name='GetGymDetailsResponse',
  full_name='pogoprotos.networking.responses.GetGymDetailsResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='gym_state', full_name='pogoprotos.networking.responses.GetGymDetailsResponse.gym_state', index=0,
      number=1, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='name', full_name='pogoprotos.networking.responses.GetGymDetailsResponse.name', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='urls', full_name='pogoprotos.networking.responses.GetGymDetailsResponse.urls', index=2,
      number=3, type=9, cpp_type=9, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='result', full_name='pogoprotos.networking.responses.GetGymDetailsResponse.result', index=3,
      number=4, type=14, cpp_type=8, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='description', full_name='pogoprotos.networking.responses.GetGymDetailsResponse.description', index=4,
      number=5, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='secondary_url', full_name='pogoprotos.networking.responses.GetGymDetailsResponse.secondary_url', index=5,
      number=6, type=9, cpp_type=9, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
    _GETGYMDETAILSRESPONSE_RESULT,
  ],
  options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=137,
  serialized_end=419,
)

_GETGYMDETAILSRESPONSE.fields_by_name['gym_state'].message_type = pogoprotos_dot_data_dot_gym_dot_gym__state__pb2._GYMSTATE
_GETGYMDETAILSRESPONSE.fields_by_name['result'].enum_type = _GETGYMDETAILSRESPONSE_RESULT
_GETGYMDETAILSRESPONSE_RESULT.containing_type = _GETGYMDETAILSRESPONSE
DESCRIPTOR.message_types_by_name['GetGymDetailsResponse'] = _GETGYMDETAILSRESPONSE
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

GetGymDetailsResponse = _reflection.GeneratedProtocolMessageType('GetGymDetailsResponse', (_message.Message,), dict(
  DESCRIPTOR = _GETGYMDETAILSRESPONSE,
  __module__ = 'pogoprotos.networking.responses.get_gym_details_response_pb2'
  # @@protoc_insertion_point(class_scope:pogoprotos.networking.responses.GetGymDetailsResponse)
  ))
_sym_db.RegisterMessage(GetGymDetailsResponse)


# @@protoc_insertion_point(module_scope)

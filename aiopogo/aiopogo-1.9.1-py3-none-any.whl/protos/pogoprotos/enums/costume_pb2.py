# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: pogoprotos/enums/costume.proto

import sys
_b=sys.version_info[0]<3 and (lambda x:x) or (lambda x:x.encode('latin1'))
from google.protobuf.internal import enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
from google.protobuf import descriptor_pb2
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor.FileDescriptor(
  name='pogoprotos/enums/costume.proto',
  package='pogoprotos.enums',
  syntax='proto3',
  serialized_pb=_b('\n\x1epogoprotos/enums/costume.proto\x12\x10pogoprotos.enums*?\n\x07\x43ostume\x12\x11\n\rCOSTUME_UNSET\x10\x00\x12\x10\n\x0cHOLIDAY_2016\x10\x01\x12\x0f\n\x0b\x41NNIVERSARY\x10\x02\x62\x06proto3')
)

_COSTUME = _descriptor.EnumDescriptor(
  name='Costume',
  full_name='pogoprotos.enums.Costume',
  filename=None,
  file=DESCRIPTOR,
  values=[
    _descriptor.EnumValueDescriptor(
      name='COSTUME_UNSET', index=0, number=0,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='HOLIDAY_2016', index=1, number=1,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='ANNIVERSARY', index=2, number=2,
      options=None,
      type=None),
  ],
  containing_type=None,
  options=None,
  serialized_start=52,
  serialized_end=115,
)
_sym_db.RegisterEnumDescriptor(_COSTUME)

Costume = enum_type_wrapper.EnumTypeWrapper(_COSTUME)
COSTUME_UNSET = 0
HOLIDAY_2016 = 1
ANNIVERSARY = 2


DESCRIPTOR.enum_types_by_name['Costume'] = _COSTUME
_sym_db.RegisterFileDescriptor(DESCRIPTOR)


# @@protoc_insertion_point(module_scope)

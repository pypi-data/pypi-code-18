# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: pogoprotos/settings/master/item/fort_modifier_attributes.proto

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
  name='pogoprotos/settings/master/item/fort_modifier_attributes.proto',
  package='pogoprotos.settings.master.item',
  syntax='proto3',
  serialized_pb=_b('\n>pogoprotos/settings/master/item/fort_modifier_attributes.proto\x12\x1fpogoprotos.settings.master.item\"b\n\x16\x46ortModifierAttributes\x12!\n\x19modifier_lifetime_seconds\x18\x01 \x01(\x05\x12%\n\x1dtroy_disk_num_pokemon_spawned\x18\x02 \x01(\x05\x62\x06proto3')
)




_FORTMODIFIERATTRIBUTES = _descriptor.Descriptor(
  name='FortModifierAttributes',
  full_name='pogoprotos.settings.master.item.FortModifierAttributes',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='modifier_lifetime_seconds', full_name='pogoprotos.settings.master.item.FortModifierAttributes.modifier_lifetime_seconds', index=0,
      number=1, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='troy_disk_num_pokemon_spawned', full_name='pogoprotos.settings.master.item.FortModifierAttributes.troy_disk_num_pokemon_spawned', index=1,
      number=2, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
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
  serialized_start=99,
  serialized_end=197,
)

DESCRIPTOR.message_types_by_name['FortModifierAttributes'] = _FORTMODIFIERATTRIBUTES
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

FortModifierAttributes = _reflection.GeneratedProtocolMessageType('FortModifierAttributes', (_message.Message,), dict(
  DESCRIPTOR = _FORTMODIFIERATTRIBUTES,
  __module__ = 'pogoprotos.settings.master.item.fort_modifier_attributes_pb2'
  # @@protoc_insertion_point(class_scope:pogoprotos.settings.master.item.FortModifierAttributes)
  ))
_sym_db.RegisterMessage(FortModifierAttributes)


# @@protoc_insertion_point(module_scope)

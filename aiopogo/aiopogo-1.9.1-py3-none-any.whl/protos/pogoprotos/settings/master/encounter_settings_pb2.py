# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: pogoprotos/settings/master/encounter_settings.proto

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
  name='pogoprotos/settings/master/encounter_settings.proto',
  package='pogoprotos.settings.master',
  syntax='proto3',
  serialized_pb=_b('\n3pogoprotos/settings/master/encounter_settings.proto\x12\x1apogoprotos.settings.master\"\xae\x01\n\x11\x45ncounterSettings\x12\x1c\n\x14spin_bonus_threshold\x18\x01 \x01(\x02\x12!\n\x19\x65xcellent_throw_threshold\x18\x02 \x01(\x02\x12\x1d\n\x15great_throw_threshold\x18\x03 \x01(\x02\x12\x1c\n\x14nice_throw_threshold\x18\x04 \x01(\x02\x12\x1b\n\x13milestone_threshold\x18\x05 \x01(\x05\x62\x06proto3')
)




_ENCOUNTERSETTINGS = _descriptor.Descriptor(
  name='EncounterSettings',
  full_name='pogoprotos.settings.master.EncounterSettings',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='spin_bonus_threshold', full_name='pogoprotos.settings.master.EncounterSettings.spin_bonus_threshold', index=0,
      number=1, type=2, cpp_type=6, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='excellent_throw_threshold', full_name='pogoprotos.settings.master.EncounterSettings.excellent_throw_threshold', index=1,
      number=2, type=2, cpp_type=6, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='great_throw_threshold', full_name='pogoprotos.settings.master.EncounterSettings.great_throw_threshold', index=2,
      number=3, type=2, cpp_type=6, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='nice_throw_threshold', full_name='pogoprotos.settings.master.EncounterSettings.nice_throw_threshold', index=3,
      number=4, type=2, cpp_type=6, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='milestone_threshold', full_name='pogoprotos.settings.master.EncounterSettings.milestone_threshold', index=4,
      number=5, type=5, cpp_type=1, label=1,
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
  serialized_start=84,
  serialized_end=258,
)

DESCRIPTOR.message_types_by_name['EncounterSettings'] = _ENCOUNTERSETTINGS
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

EncounterSettings = _reflection.GeneratedProtocolMessageType('EncounterSettings', (_message.Message,), dict(
  DESCRIPTOR = _ENCOUNTERSETTINGS,
  __module__ = 'pogoprotos.settings.master.encounter_settings_pb2'
  # @@protoc_insertion_point(class_scope:pogoprotos.settings.master.EncounterSettings)
  ))
_sym_db.RegisterMessage(EncounterSettings)


# @@protoc_insertion_point(module_scope)

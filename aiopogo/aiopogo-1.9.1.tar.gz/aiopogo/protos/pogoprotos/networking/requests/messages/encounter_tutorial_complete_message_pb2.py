# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: pogoprotos/networking/requests/messages/encounter_tutorial_complete_message.proto

import sys
_b=sys.version_info[0]<3 and (lambda x:x) or (lambda x:x.encode('latin1'))
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
from google.protobuf import descriptor_pb2
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from pogoprotos.enums import pokemon_id_pb2 as pogoprotos_dot_enums_dot_pokemon__id__pb2


DESCRIPTOR = _descriptor.FileDescriptor(
  name='pogoprotos/networking/requests/messages/encounter_tutorial_complete_message.proto',
  package='pogoprotos.networking.requests.messages',
  syntax='proto3',
  serialized_pb=_b('\nQpogoprotos/networking/requests/messages/encounter_tutorial_complete_message.proto\x12\'pogoprotos.networking.requests.messages\x1a!pogoprotos/enums/pokemon_id.proto\"S\n EncounterTutorialCompleteMessage\x12/\n\npokemon_id\x18\x01 \x01(\x0e\x32\x1b.pogoprotos.enums.PokemonIdb\x06proto3')
  ,
  dependencies=[pogoprotos_dot_enums_dot_pokemon__id__pb2.DESCRIPTOR,])




_ENCOUNTERTUTORIALCOMPLETEMESSAGE = _descriptor.Descriptor(
  name='EncounterTutorialCompleteMessage',
  full_name='pogoprotos.networking.requests.messages.EncounterTutorialCompleteMessage',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='pokemon_id', full_name='pogoprotos.networking.requests.messages.EncounterTutorialCompleteMessage.pokemon_id', index=0,
      number=1, type=14, cpp_type=8, label=1,
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
  serialized_start=161,
  serialized_end=244,
)

_ENCOUNTERTUTORIALCOMPLETEMESSAGE.fields_by_name['pokemon_id'].enum_type = pogoprotos_dot_enums_dot_pokemon__id__pb2._POKEMONID
DESCRIPTOR.message_types_by_name['EncounterTutorialCompleteMessage'] = _ENCOUNTERTUTORIALCOMPLETEMESSAGE
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

EncounterTutorialCompleteMessage = _reflection.GeneratedProtocolMessageType('EncounterTutorialCompleteMessage', (_message.Message,), dict(
  DESCRIPTOR = _ENCOUNTERTUTORIALCOMPLETEMESSAGE,
  __module__ = 'pogoprotos.networking.requests.messages.encounter_tutorial_complete_message_pb2'
  # @@protoc_insertion_point(class_scope:pogoprotos.networking.requests.messages.EncounterTutorialCompleteMessage)
  ))
_sym_db.RegisterMessage(EncounterTutorialCompleteMessage)


# @@protoc_insertion_point(module_scope)

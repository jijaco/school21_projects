# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: ships.proto
# Protobuf Python Version: 5.26.1
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x0bships.proto\"\x96\x03\n\tSpaceship\x12+\n\tAlignment\x18\x01 \x01(\x0e\x32\x18.Spaceship.AlignmentType\x12\x15\n\x04name\x18\x02 \x01(\t:\x07Unknown\x12\x0e\n\x06length\x18\x03 \x01(\x02\x12#\n\x05\x43lass\x18\x04 \x01(\x0e\x32\x14.Spaceship.ClassType\x12\x0c\n\x04size\x18\x05 \x01(\x05\x12\x14\n\x0c\x61rmed_status\x18\x06 \x01(\x08\x12$\n\x08officers\x18\x07 \x03(\x0b\x32\x12.Spaceship.Officer\x1a>\n\x07Officer\x12\x12\n\nfirst_name\x18\x01 \x01(\t\x12\x11\n\tlast_name\x18\x02 \x01(\t\x12\x0c\n\x04rank\x18\x03 \x01(\t\"$\n\rAlignmentType\x12\x08\n\x04\x41LLY\x10\x00\x12\t\n\x05\x45NEMY\x10\x01\"`\n\tClassType\x12\x0c\n\x08\x43ORVETTE\x10\x00\x12\x0b\n\x07\x46RIGATE\x10\x01\x12\x0b\n\x07\x43RUISER\x10\x02\x12\r\n\tDESTROYER\x10\x03\x12\x0b\n\x07\x43\x41RRIER\x10\x04\x12\x0f\n\x0b\x44READNOUGHT\x10\x05\"\xc4\x01\n\nCoordinate\x12\x1d\n\x15right_ascension_hours\x18\x01 \x01(\x01\x12\x1f\n\x17right_ascension_minutes\x18\x02 \x01(\x01\x12\x1f\n\x17right_ascension_seconds\x18\x03 \x01(\x01\x12\x1b\n\x13\x64\x65\x63lination_degrees\x18\x04 \x01(\x01\x12\x1b\n\x13\x64\x65\x63lination_minutes\x18\x05 \x01(\x01\x12\x1b\n\x13\x64\x65\x63lination_seconds\x18\x06 \x01(\x01\"T\n\x12RequestedSpaceship\x12\x1f\n\ncoordinate\x18\x01 \x01(\x0b\x32\x0b.Coordinate\x12\x1d\n\tspaceship\x18\x02 \x03(\x0b\x32\n.Spaceship\"+\n\nSpaceships\x12\x1d\n\tspaceship\x18\x01 \x03(\x0b\x32\n.Spaceship\"L\n\x19SpaceshipLocationDatabase\x12/\n\x12requestedspaceship\x18\x01 \x03(\x0b\x32\x13.RequestedSpaceship\"4\n\x1eStringSpaceshipsRepresentation\x12\x12\n\nspaceships\x18\x01 \x01(\t2@\n\x10LocatedSpaceship\x12,\n\rGetCoordinate\x12\x0b.Coordinate\x1a\n.Spaceship\"\x00\x30\x01')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'ships_pb2', _globals)
if not _descriptor._USE_C_DESCRIPTORS:
  DESCRIPTOR._loaded_options = None
  _globals['_SPACESHIP']._serialized_start=16
  _globals['_SPACESHIP']._serialized_end=422
  _globals['_SPACESHIP_OFFICER']._serialized_start=224
  _globals['_SPACESHIP_OFFICER']._serialized_end=286
  _globals['_SPACESHIP_ALIGNMENTTYPE']._serialized_start=288
  _globals['_SPACESHIP_ALIGNMENTTYPE']._serialized_end=324
  _globals['_SPACESHIP_CLASSTYPE']._serialized_start=326
  _globals['_SPACESHIP_CLASSTYPE']._serialized_end=422
  _globals['_COORDINATE']._serialized_start=425
  _globals['_COORDINATE']._serialized_end=621
  _globals['_REQUESTEDSPACESHIP']._serialized_start=623
  _globals['_REQUESTEDSPACESHIP']._serialized_end=707
  _globals['_SPACESHIPS']._serialized_start=709
  _globals['_SPACESHIPS']._serialized_end=752
  _globals['_SPACESHIPLOCATIONDATABASE']._serialized_start=754
  _globals['_SPACESHIPLOCATIONDATABASE']._serialized_end=830
  _globals['_STRINGSPACESHIPSREPRESENTATION']._serialized_start=832
  _globals['_STRINGSPACESHIPSREPRESENTATION']._serialized_end=884
  _globals['_LOCATEDSPACESHIP']._serialized_start=886
  _globals['_LOCATEDSPACESHIP']._serialized_end=950
# @@protoc_insertion_point(module_scope)
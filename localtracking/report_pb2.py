# Generated by the protocol buffer compiler.  DO NOT EDIT!

from google.protobuf import descriptor
from google.protobuf import message
from google.protobuf import reflection
from google.protobuf import descriptor_pb2
# @@protoc_insertion_point(imports)



DESCRIPTOR = descriptor.FileDescriptor(
  name='report.proto',
  package='',
  serialized_pb='\n\x0creport.proto\"F\n\x07Station\x12\x0b\n\x03mac\x18\x01 \x02(\x0c\x12\x11\n\ttimestamp\x18\x02 \x02(\x05\x12\x0c\n\x04rssi\x18\x03 \x02(\x05\x12\r\n\x05\x63ount\x18\x04 \x02(\x05\"U\n\x06Report\x12\x0f\n\x07version\x18\x01 \x02(\x05\x12\x11\n\ttimestamp\x18\x02 \x02(\x04\x12\x0b\n\x03mac\x18\x03 \x02(\x0c\x12\x1a\n\x08stations\x18\x04 \x03(\x0b\x32\x08.Station')




_STATION = descriptor.Descriptor(
  name='Station',
  full_name='Station',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    descriptor.FieldDescriptor(
      name='mac', full_name='Station.mac', index=0,
      number=1, type=12, cpp_type=9, label=2,
      has_default_value=False, default_value="",
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='timestamp', full_name='Station.timestamp', index=1,
      number=2, type=5, cpp_type=1, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='rssi', full_name='Station.rssi', index=2,
      number=3, type=5, cpp_type=1, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='count', full_name='Station.count', index=3,
      number=4, type=5, cpp_type=1, label=2,
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
  extension_ranges=[],
  serialized_start=16,
  serialized_end=86,
)


_REPORT = descriptor.Descriptor(
  name='Report',
  full_name='Report',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    descriptor.FieldDescriptor(
      name='version', full_name='Report.version', index=0,
      number=1, type=5, cpp_type=1, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='timestamp', full_name='Report.timestamp', index=1,
      number=2, type=4, cpp_type=4, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='mac', full_name='Report.mac', index=2,
      number=3, type=12, cpp_type=9, label=2,
      has_default_value=False, default_value="",
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='stations', full_name='Report.stations', index=3,
      number=4, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
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
  extension_ranges=[],
  serialized_start=88,
  serialized_end=173,
)

_REPORT.fields_by_name['stations'].message_type = _STATION
DESCRIPTOR.message_types_by_name['Station'] = _STATION
DESCRIPTOR.message_types_by_name['Report'] = _REPORT

class Station(message.Message):
  __metaclass__ = reflection.GeneratedProtocolMessageType
  DESCRIPTOR = _STATION
  
  # @@protoc_insertion_point(class_scope:Station)

class Report(message.Message):
  __metaclass__ = reflection.GeneratedProtocolMessageType
  DESCRIPTOR = _REPORT
  
  # @@protoc_insertion_point(class_scope:Report)

# @@protoc_insertion_point(module_scope)

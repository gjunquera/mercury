# Generated by the protocol buffer compiler.  DO NOT EDIT!

from google.protobuf import descriptor
from google.protobuf import message
from google.protobuf import reflection
from google.protobuf import descriptor_pb2
# @@protoc_insertion_point(imports)



DESCRIPTOR = descriptor.FileDescriptor(
  name='Message.proto',
  package='com.mwr.mercury',
  serialized_pb='\n\rMessage.proto\x12\x0f\x63om.mwr.mercury\"S\n\x07Request\x12\x0f\n\x07section\x18\x01 \x01(\t\x12\x10\n\x08\x66unction\x18\x02 \x01(\t\x12%\n\x04\x61rgs\x18\x03 \x03(\x0b\x32\x17.com.mwr.mercury.KVPair\"Y\n\x08Response\x12\x0c\n\x04\x64\x61ta\x18\x01 \x01(\x0c\x12\r\n\x05\x65rror\x18\x02 \x01(\x0c\x12\x30\n\x0fstructured_data\x18\x03 \x03(\x0b\x32\x17.com.mwr.mercury.KVPair\"$\n\x06KVPair\x12\x0b\n\x03key\x18\x01 \x02(\t\x12\r\n\x05value\x18\x02 \x03(\x0c\"\xbc\x03\n\x10ProviderResponse\x12\x34\n\x04info\x18\x01 \x03(\x0b\x32&.com.mwr.mercury.ProviderResponse.Info\x1a\xf1\x02\n\x04Info\x12\x11\n\tauthority\x18\x01 \x01(\t\x12\x13\n\x0bpackageName\x18\x02 \x01(\t\x12\x16\n\x0ereadPermission\x18\x03 \x01(\t\x12\x1d\n\x15uriPermissionPatterns\x18\x04 \x03(\t\x12\x17\n\x0fwritePermission\x18\x05 \x01(\t\x12Q\n\x0fpathPermissions\x18\x06 \x03(\x0b\x32\x38.com.mwr.mercury.ProviderResponse.Info.PatternPermission\x12\x14\n\x0cmultiprocess\x18\x07 \x01(\x08\x12\x1b\n\x13grantUriPermissions\x18\x08 \x01(\x08\x1ak\n\x11PatternPermission\x12\x17\n\x0fwritePermission\x18\x01 \x01(\t\x12\x16\n\x0ereadPermission\x18\x02 \x01(\t\x12\x12\n\nwriteNeeds\x18\x03 \x01(\t\x12\x11\n\treadNeeds\x18\x04 \x01(\t\"\x94\x03\n\x0fPackageResponse\x12\x33\n\x04info\x18\x01 \x03(\x0b\x32%.com.mwr.mercury.PackageResponse.Info\x12=\n\tsharedUid\x18\x02 \x03(\x0b\x32*.com.mwr.mercury.PackageResponse.SharedUid\x1a\xc7\x01\n\x04Info\x12\x13\n\x0bpackageName\x18\x01 \x01(\t\x12\x13\n\x0bprocessName\x18\x02 \x01(\t\x12\x0f\n\x07version\x18\x03 \x01(\t\x12\x15\n\rdataDirectory\x18\x04 \x01(\t\x12\x0f\n\x07\x61pkPath\x18\x05 \x01(\t\x12\x0b\n\x03uid\x18\x06 \x01(\x05\x12\x0c\n\x04guid\x18\x07 \x03(\x05\x12\x14\n\x0csharedUserId\x18\x08 \x01(\t\x12\x17\n\x0fsharedLibraries\x18\t \x03(\t\x12\x12\n\npermission\x18\n \x03(\t\x1a\x43\n\tSharedUid\x12\x14\n\x0cpackageNames\x18\x01 \x03(\t\x12\x0b\n\x03uid\x18\x02 \x01(\x05\x12\x13\n\x0bpermissions\x18\x03 \x03(\t\"\x88\x01\n\x0fServiceResponse\x12\x33\n\x04info\x18\x01 \x03(\x0b\x32%.com.mwr.mercury.ServiceResponse.Info\x1a@\n\x04Info\x12\x13\n\x0bpackageName\x18\x01 \x01(\t\x12\x0f\n\x07service\x18\x02 \x01(\t\x12\x12\n\npermission\x18\x03 \x01(\t\"w\n\x10\x41\x63tivityResponse\x12\x34\n\x04info\x18\x01 \x03(\x0b\x32&.com.mwr.mercury.ActivityResponse.Info\x1a-\n\x04Info\x12\x13\n\x0bpackageName\x18\x01 \x01(\t\x12\x10\n\x08\x61\x63tivity\x18\x03 \x01(\t\"\x8d\x01\n\x11\x42roadcastResponse\x12\x35\n\x04info\x18\x01 \x03(\x0b\x32\'.com.mwr.mercury.BroadcastResponse.Info\x1a\x41\n\x04Info\x12\x13\n\x0bpackageName\x18\x01 \x01(\t\x12\x10\n\x08receiver\x18\x02 \x01(\t\x12\x12\n\npermission\x18\x03 \x01(\t\"\x80\x01\n\rDebugResponse\x12\x31\n\x04info\x18\x01 \x03(\x0b\x32#.com.mwr.mercury.DebugResponse.Info\x1a<\n\x04Info\x12\x13\n\x0bpackageName\x18\x01 \x01(\t\x12\x0b\n\x03uid\x18\x02 \x01(\x05\x12\x12\n\npermission\x18\x03 \x03(\t\"t\n\x0eNativeResponse\x12\x32\n\x04info\x18\x01 \x03(\x0b\x32$.com.mwr.mercury.NativeResponse.Info\x1a.\n\x04Info\x12\x13\n\x0bpackageName\x18\x01 \x01(\t\x12\x11\n\tnativeLib\x18\x02 \x03(\t')




_REQUEST = descriptor.Descriptor(
  name='Request',
  full_name='com.mwr.mercury.Request',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    descriptor.FieldDescriptor(
      name='section', full_name='com.mwr.mercury.Request.section', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=unicode("", "utf-8"),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='function', full_name='com.mwr.mercury.Request.function', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=unicode("", "utf-8"),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='args', full_name='com.mwr.mercury.Request.args', index=2,
      number=3, type=11, cpp_type=10, label=3,
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
  serialized_start=34,
  serialized_end=117,
)


_RESPONSE = descriptor.Descriptor(
  name='Response',
  full_name='com.mwr.mercury.Response',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    descriptor.FieldDescriptor(
      name='data', full_name='com.mwr.mercury.Response.data', index=0,
      number=1, type=12, cpp_type=9, label=1,
      has_default_value=False, default_value="",
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='error', full_name='com.mwr.mercury.Response.error', index=1,
      number=2, type=12, cpp_type=9, label=1,
      has_default_value=False, default_value="",
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='structured_data', full_name='com.mwr.mercury.Response.structured_data', index=2,
      number=3, type=11, cpp_type=10, label=3,
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
  serialized_start=119,
  serialized_end=208,
)


_KVPAIR = descriptor.Descriptor(
  name='KVPair',
  full_name='com.mwr.mercury.KVPair',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    descriptor.FieldDescriptor(
      name='key', full_name='com.mwr.mercury.KVPair.key', index=0,
      number=1, type=9, cpp_type=9, label=2,
      has_default_value=False, default_value=unicode("", "utf-8"),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='value', full_name='com.mwr.mercury.KVPair.value', index=1,
      number=2, type=12, cpp_type=9, label=3,
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
  serialized_start=210,
  serialized_end=246,
)


_PROVIDERRESPONSE_INFO_PATTERNPERMISSION = descriptor.Descriptor(
  name='PatternPermission',
  full_name='com.mwr.mercury.ProviderResponse.Info.PatternPermission',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    descriptor.FieldDescriptor(
      name='writePermission', full_name='com.mwr.mercury.ProviderResponse.Info.PatternPermission.writePermission', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=unicode("", "utf-8"),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='readPermission', full_name='com.mwr.mercury.ProviderResponse.Info.PatternPermission.readPermission', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=unicode("", "utf-8"),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='writeNeeds', full_name='com.mwr.mercury.ProviderResponse.Info.PatternPermission.writeNeeds', index=2,
      number=3, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=unicode("", "utf-8"),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='readNeeds', full_name='com.mwr.mercury.ProviderResponse.Info.PatternPermission.readNeeds', index=3,
      number=4, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=unicode("", "utf-8"),
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
  serialized_start=586,
  serialized_end=693,
)

_PROVIDERRESPONSE_INFO = descriptor.Descriptor(
  name='Info',
  full_name='com.mwr.mercury.ProviderResponse.Info',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    descriptor.FieldDescriptor(
      name='authority', full_name='com.mwr.mercury.ProviderResponse.Info.authority', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=unicode("", "utf-8"),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='packageName', full_name='com.mwr.mercury.ProviderResponse.Info.packageName', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=unicode("", "utf-8"),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='readPermission', full_name='com.mwr.mercury.ProviderResponse.Info.readPermission', index=2,
      number=3, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=unicode("", "utf-8"),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='uriPermissionPatterns', full_name='com.mwr.mercury.ProviderResponse.Info.uriPermissionPatterns', index=3,
      number=4, type=9, cpp_type=9, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='writePermission', full_name='com.mwr.mercury.ProviderResponse.Info.writePermission', index=4,
      number=5, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=unicode("", "utf-8"),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='pathPermissions', full_name='com.mwr.mercury.ProviderResponse.Info.pathPermissions', index=5,
      number=6, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='multiprocess', full_name='com.mwr.mercury.ProviderResponse.Info.multiprocess', index=6,
      number=7, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='grantUriPermissions', full_name='com.mwr.mercury.ProviderResponse.Info.grantUriPermissions', index=7,
      number=8, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[_PROVIDERRESPONSE_INFO_PATTERNPERMISSION, ],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  extension_ranges=[],
  serialized_start=324,
  serialized_end=693,
)

_PROVIDERRESPONSE = descriptor.Descriptor(
  name='ProviderResponse',
  full_name='com.mwr.mercury.ProviderResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    descriptor.FieldDescriptor(
      name='info', full_name='com.mwr.mercury.ProviderResponse.info', index=0,
      number=1, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[_PROVIDERRESPONSE_INFO, ],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  extension_ranges=[],
  serialized_start=249,
  serialized_end=693,
)


_PACKAGERESPONSE_INFO = descriptor.Descriptor(
  name='Info',
  full_name='com.mwr.mercury.PackageResponse.Info',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    descriptor.FieldDescriptor(
      name='packageName', full_name='com.mwr.mercury.PackageResponse.Info.packageName', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=unicode("", "utf-8"),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='processName', full_name='com.mwr.mercury.PackageResponse.Info.processName', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=unicode("", "utf-8"),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='version', full_name='com.mwr.mercury.PackageResponse.Info.version', index=2,
      number=3, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=unicode("", "utf-8"),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='dataDirectory', full_name='com.mwr.mercury.PackageResponse.Info.dataDirectory', index=3,
      number=4, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=unicode("", "utf-8"),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='apkPath', full_name='com.mwr.mercury.PackageResponse.Info.apkPath', index=4,
      number=5, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=unicode("", "utf-8"),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='uid', full_name='com.mwr.mercury.PackageResponse.Info.uid', index=5,
      number=6, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='guid', full_name='com.mwr.mercury.PackageResponse.Info.guid', index=6,
      number=7, type=5, cpp_type=1, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='sharedUserId', full_name='com.mwr.mercury.PackageResponse.Info.sharedUserId', index=7,
      number=8, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=unicode("", "utf-8"),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='sharedLibraries', full_name='com.mwr.mercury.PackageResponse.Info.sharedLibraries', index=8,
      number=9, type=9, cpp_type=9, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='permission', full_name='com.mwr.mercury.PackageResponse.Info.permission', index=9,
      number=10, type=9, cpp_type=9, label=3,
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
  serialized_start=832,
  serialized_end=1031,
)

_PACKAGERESPONSE_SHAREDUID = descriptor.Descriptor(
  name='SharedUid',
  full_name='com.mwr.mercury.PackageResponse.SharedUid',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    descriptor.FieldDescriptor(
      name='packageNames', full_name='com.mwr.mercury.PackageResponse.SharedUid.packageNames', index=0,
      number=1, type=9, cpp_type=9, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='uid', full_name='com.mwr.mercury.PackageResponse.SharedUid.uid', index=1,
      number=2, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='permissions', full_name='com.mwr.mercury.PackageResponse.SharedUid.permissions', index=2,
      number=3, type=9, cpp_type=9, label=3,
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
  serialized_start=1033,
  serialized_end=1100,
)

_PACKAGERESPONSE = descriptor.Descriptor(
  name='PackageResponse',
  full_name='com.mwr.mercury.PackageResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    descriptor.FieldDescriptor(
      name='info', full_name='com.mwr.mercury.PackageResponse.info', index=0,
      number=1, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='sharedUid', full_name='com.mwr.mercury.PackageResponse.sharedUid', index=1,
      number=2, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[_PACKAGERESPONSE_INFO, _PACKAGERESPONSE_SHAREDUID, ],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  extension_ranges=[],
  serialized_start=696,
  serialized_end=1100,
)


_SERVICERESPONSE_INFO = descriptor.Descriptor(
  name='Info',
  full_name='com.mwr.mercury.ServiceResponse.Info',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    descriptor.FieldDescriptor(
      name='packageName', full_name='com.mwr.mercury.ServiceResponse.Info.packageName', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=unicode("", "utf-8"),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='service', full_name='com.mwr.mercury.ServiceResponse.Info.service', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=unicode("", "utf-8"),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='permission', full_name='com.mwr.mercury.ServiceResponse.Info.permission', index=2,
      number=3, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=unicode("", "utf-8"),
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
  serialized_start=1175,
  serialized_end=1239,
)

_SERVICERESPONSE = descriptor.Descriptor(
  name='ServiceResponse',
  full_name='com.mwr.mercury.ServiceResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    descriptor.FieldDescriptor(
      name='info', full_name='com.mwr.mercury.ServiceResponse.info', index=0,
      number=1, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[_SERVICERESPONSE_INFO, ],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  extension_ranges=[],
  serialized_start=1103,
  serialized_end=1239,
)


_ACTIVITYRESPONSE_INFO = descriptor.Descriptor(
  name='Info',
  full_name='com.mwr.mercury.ActivityResponse.Info',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    descriptor.FieldDescriptor(
      name='packageName', full_name='com.mwr.mercury.ActivityResponse.Info.packageName', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=unicode("", "utf-8"),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='activity', full_name='com.mwr.mercury.ActivityResponse.Info.activity', index=1,
      number=3, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=unicode("", "utf-8"),
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
  serialized_start=1315,
  serialized_end=1360,
)

_ACTIVITYRESPONSE = descriptor.Descriptor(
  name='ActivityResponse',
  full_name='com.mwr.mercury.ActivityResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    descriptor.FieldDescriptor(
      name='info', full_name='com.mwr.mercury.ActivityResponse.info', index=0,
      number=1, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[_ACTIVITYRESPONSE_INFO, ],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  extension_ranges=[],
  serialized_start=1241,
  serialized_end=1360,
)


_BROADCASTRESPONSE_INFO = descriptor.Descriptor(
  name='Info',
  full_name='com.mwr.mercury.BroadcastResponse.Info',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    descriptor.FieldDescriptor(
      name='packageName', full_name='com.mwr.mercury.BroadcastResponse.Info.packageName', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=unicode("", "utf-8"),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='receiver', full_name='com.mwr.mercury.BroadcastResponse.Info.receiver', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=unicode("", "utf-8"),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='permission', full_name='com.mwr.mercury.BroadcastResponse.Info.permission', index=2,
      number=3, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=unicode("", "utf-8"),
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
  serialized_start=1439,
  serialized_end=1504,
)

_BROADCASTRESPONSE = descriptor.Descriptor(
  name='BroadcastResponse',
  full_name='com.mwr.mercury.BroadcastResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    descriptor.FieldDescriptor(
      name='info', full_name='com.mwr.mercury.BroadcastResponse.info', index=0,
      number=1, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[_BROADCASTRESPONSE_INFO, ],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  extension_ranges=[],
  serialized_start=1363,
  serialized_end=1504,
)


_DEBUGRESPONSE_INFO = descriptor.Descriptor(
  name='Info',
  full_name='com.mwr.mercury.DebugResponse.Info',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    descriptor.FieldDescriptor(
      name='packageName', full_name='com.mwr.mercury.DebugResponse.Info.packageName', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=unicode("", "utf-8"),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='uid', full_name='com.mwr.mercury.DebugResponse.Info.uid', index=1,
      number=2, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='permission', full_name='com.mwr.mercury.DebugResponse.Info.permission', index=2,
      number=3, type=9, cpp_type=9, label=3,
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
  serialized_start=1575,
  serialized_end=1635,
)

_DEBUGRESPONSE = descriptor.Descriptor(
  name='DebugResponse',
  full_name='com.mwr.mercury.DebugResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    descriptor.FieldDescriptor(
      name='info', full_name='com.mwr.mercury.DebugResponse.info', index=0,
      number=1, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[_DEBUGRESPONSE_INFO, ],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  extension_ranges=[],
  serialized_start=1507,
  serialized_end=1635,
)


_NATIVERESPONSE_INFO = descriptor.Descriptor(
  name='Info',
  full_name='com.mwr.mercury.NativeResponse.Info',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    descriptor.FieldDescriptor(
      name='packageName', full_name='com.mwr.mercury.NativeResponse.Info.packageName', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=unicode("", "utf-8"),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='nativeLib', full_name='com.mwr.mercury.NativeResponse.Info.nativeLib', index=1,
      number=2, type=9, cpp_type=9, label=3,
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
  serialized_start=1707,
  serialized_end=1753,
)

_NATIVERESPONSE = descriptor.Descriptor(
  name='NativeResponse',
  full_name='com.mwr.mercury.NativeResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    descriptor.FieldDescriptor(
      name='info', full_name='com.mwr.mercury.NativeResponse.info', index=0,
      number=1, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[_NATIVERESPONSE_INFO, ],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  extension_ranges=[],
  serialized_start=1637,
  serialized_end=1753,
)

_REQUEST.fields_by_name['args'].message_type = _KVPAIR
_RESPONSE.fields_by_name['structured_data'].message_type = _KVPAIR
_PROVIDERRESPONSE_INFO_PATTERNPERMISSION.containing_type = _PROVIDERRESPONSE_INFO;
_PROVIDERRESPONSE_INFO.fields_by_name['pathPermissions'].message_type = _PROVIDERRESPONSE_INFO_PATTERNPERMISSION
_PROVIDERRESPONSE_INFO.containing_type = _PROVIDERRESPONSE;
_PROVIDERRESPONSE.fields_by_name['info'].message_type = _PROVIDERRESPONSE_INFO
_PACKAGERESPONSE_INFO.containing_type = _PACKAGERESPONSE;
_PACKAGERESPONSE_SHAREDUID.containing_type = _PACKAGERESPONSE;
_PACKAGERESPONSE.fields_by_name['info'].message_type = _PACKAGERESPONSE_INFO
_PACKAGERESPONSE.fields_by_name['sharedUid'].message_type = _PACKAGERESPONSE_SHAREDUID
_SERVICERESPONSE_INFO.containing_type = _SERVICERESPONSE;
_SERVICERESPONSE.fields_by_name['info'].message_type = _SERVICERESPONSE_INFO
_ACTIVITYRESPONSE_INFO.containing_type = _ACTIVITYRESPONSE;
_ACTIVITYRESPONSE.fields_by_name['info'].message_type = _ACTIVITYRESPONSE_INFO
_BROADCASTRESPONSE_INFO.containing_type = _BROADCASTRESPONSE;
_BROADCASTRESPONSE.fields_by_name['info'].message_type = _BROADCASTRESPONSE_INFO
_DEBUGRESPONSE_INFO.containing_type = _DEBUGRESPONSE;
_DEBUGRESPONSE.fields_by_name['info'].message_type = _DEBUGRESPONSE_INFO
_NATIVERESPONSE_INFO.containing_type = _NATIVERESPONSE;
_NATIVERESPONSE.fields_by_name['info'].message_type = _NATIVERESPONSE_INFO
DESCRIPTOR.message_types_by_name['Request'] = _REQUEST
DESCRIPTOR.message_types_by_name['Response'] = _RESPONSE
DESCRIPTOR.message_types_by_name['KVPair'] = _KVPAIR
DESCRIPTOR.message_types_by_name['ProviderResponse'] = _PROVIDERRESPONSE
DESCRIPTOR.message_types_by_name['PackageResponse'] = _PACKAGERESPONSE
DESCRIPTOR.message_types_by_name['ServiceResponse'] = _SERVICERESPONSE
DESCRIPTOR.message_types_by_name['ActivityResponse'] = _ACTIVITYRESPONSE
DESCRIPTOR.message_types_by_name['BroadcastResponse'] = _BROADCASTRESPONSE
DESCRIPTOR.message_types_by_name['DebugResponse'] = _DEBUGRESPONSE
DESCRIPTOR.message_types_by_name['NativeResponse'] = _NATIVERESPONSE

class Request(message.Message):
  __metaclass__ = reflection.GeneratedProtocolMessageType
  DESCRIPTOR = _REQUEST
  
  # @@protoc_insertion_point(class_scope:com.mwr.mercury.Request)

class Response(message.Message):
  __metaclass__ = reflection.GeneratedProtocolMessageType
  DESCRIPTOR = _RESPONSE
  
  # @@protoc_insertion_point(class_scope:com.mwr.mercury.Response)

class KVPair(message.Message):
  __metaclass__ = reflection.GeneratedProtocolMessageType
  DESCRIPTOR = _KVPAIR
  
  # @@protoc_insertion_point(class_scope:com.mwr.mercury.KVPair)

class ProviderResponse(message.Message):
  __metaclass__ = reflection.GeneratedProtocolMessageType
  
  class Info(message.Message):
    __metaclass__ = reflection.GeneratedProtocolMessageType
    
    class PatternPermission(message.Message):
      __metaclass__ = reflection.GeneratedProtocolMessageType
      DESCRIPTOR = _PROVIDERRESPONSE_INFO_PATTERNPERMISSION
      
      # @@protoc_insertion_point(class_scope:com.mwr.mercury.ProviderResponse.Info.PatternPermission)
    DESCRIPTOR = _PROVIDERRESPONSE_INFO
    
    # @@protoc_insertion_point(class_scope:com.mwr.mercury.ProviderResponse.Info)
  DESCRIPTOR = _PROVIDERRESPONSE
  
  # @@protoc_insertion_point(class_scope:com.mwr.mercury.ProviderResponse)

class PackageResponse(message.Message):
  __metaclass__ = reflection.GeneratedProtocolMessageType
  
  class Info(message.Message):
    __metaclass__ = reflection.GeneratedProtocolMessageType
    DESCRIPTOR = _PACKAGERESPONSE_INFO
    
    # @@protoc_insertion_point(class_scope:com.mwr.mercury.PackageResponse.Info)
  
  class SharedUid(message.Message):
    __metaclass__ = reflection.GeneratedProtocolMessageType
    DESCRIPTOR = _PACKAGERESPONSE_SHAREDUID
    
    # @@protoc_insertion_point(class_scope:com.mwr.mercury.PackageResponse.SharedUid)
  DESCRIPTOR = _PACKAGERESPONSE
  
  # @@protoc_insertion_point(class_scope:com.mwr.mercury.PackageResponse)

class ServiceResponse(message.Message):
  __metaclass__ = reflection.GeneratedProtocolMessageType
  
  class Info(message.Message):
    __metaclass__ = reflection.GeneratedProtocolMessageType
    DESCRIPTOR = _SERVICERESPONSE_INFO
    
    # @@protoc_insertion_point(class_scope:com.mwr.mercury.ServiceResponse.Info)
  DESCRIPTOR = _SERVICERESPONSE
  
  # @@protoc_insertion_point(class_scope:com.mwr.mercury.ServiceResponse)

class ActivityResponse(message.Message):
  __metaclass__ = reflection.GeneratedProtocolMessageType
  
  class Info(message.Message):
    __metaclass__ = reflection.GeneratedProtocolMessageType
    DESCRIPTOR = _ACTIVITYRESPONSE_INFO
    
    # @@protoc_insertion_point(class_scope:com.mwr.mercury.ActivityResponse.Info)
  DESCRIPTOR = _ACTIVITYRESPONSE
  
  # @@protoc_insertion_point(class_scope:com.mwr.mercury.ActivityResponse)

class BroadcastResponse(message.Message):
  __metaclass__ = reflection.GeneratedProtocolMessageType
  
  class Info(message.Message):
    __metaclass__ = reflection.GeneratedProtocolMessageType
    DESCRIPTOR = _BROADCASTRESPONSE_INFO
    
    # @@protoc_insertion_point(class_scope:com.mwr.mercury.BroadcastResponse.Info)
  DESCRIPTOR = _BROADCASTRESPONSE
  
  # @@protoc_insertion_point(class_scope:com.mwr.mercury.BroadcastResponse)

class DebugResponse(message.Message):
  __metaclass__ = reflection.GeneratedProtocolMessageType
  
  class Info(message.Message):
    __metaclass__ = reflection.GeneratedProtocolMessageType
    DESCRIPTOR = _DEBUGRESPONSE_INFO
    
    # @@protoc_insertion_point(class_scope:com.mwr.mercury.DebugResponse.Info)
  DESCRIPTOR = _DEBUGRESPONSE
  
  # @@protoc_insertion_point(class_scope:com.mwr.mercury.DebugResponse)

class NativeResponse(message.Message):
  __metaclass__ = reflection.GeneratedProtocolMessageType
  
  class Info(message.Message):
    __metaclass__ = reflection.GeneratedProtocolMessageType
    DESCRIPTOR = _NATIVERESPONSE_INFO
    
    # @@protoc_insertion_point(class_scope:com.mwr.mercury.NativeResponse.Info)
  DESCRIPTOR = _NATIVERESPONSE
  
  # @@protoc_insertion_point(class_scope:com.mwr.mercury.NativeResponse)

# @@protoc_insertion_point(module_scope)

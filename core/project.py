from idc import *

# from core.logger import logger
from core.objects import GUID, Structure, Pointer, ImportProtocol, ExportProtocol
from core.utils import find_object, filter_objects


IMPORT_PROTOCOL = 0
EXPORT_PROTOCOL = 1


class ProtocolsList:

    def __init__(self):
        self.__protocols = {}

    def __iter__(self):
        return iter(self.__protocols.values())

    def __len__(self):
        return len(self.__protocols.values())

    def is_registered(self, guid):
        return guid in self.__protocols

    def find(self, guid):
        return self.__protocols.get(guid)

    def register(self, guid, struc, interface_ptr, introduced_at, type):
        if self.is_registered(guid):
            raise Exception("Attempt to register alredy registered protocol: %s" % struc.name)
        if type == IMPORT_PROTOCOL:
            protocol_class = ImportProtocol
        elif type == EXPORT_PROTOCOL:
            protocol_class = ExportProtocol
        else:
            raise ValueError('type')
        protocol = protocol_class(guid, struc, interface_ptr, introduced_at)
        self.__protocols[guid] = protocol
        return protocol


protocols = ProtocolsList()
import_protocol_name_prefix = "UNKNOWN"
export_protocol_name_prefix = "UNKNOWN"
autogen_struct_prefix = "UNKNOWN"


def load_til(path_to_til):
    if LoadTil(path_to_til) != 1:
       raise Exception("LoadTil('%s') has failed" % (path_to_til))

    # Fix UINTN to be the actual word size if we can determine it
    Til2Idb(-1, "UINTN")
    entry = GetEntryPoint(GetEntryOrdinal(0))
    if entry != BADADDR:
        typedef = "typedef UINT" + str(16 << GetSegmentAttr(entry, SEGATTR_BITNESS)) + " UINTN;"
        for i in xrange(0, GetMaxLocalType()):
            if GetLocalTypeName(i) == "UINTN":
                SetLocalType(SetLocalType(i, "", 0), typedef, 0)

def load_project(path):
    pass

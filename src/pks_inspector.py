'''
Created on 25 Jan 2018

@author: mike_000
'''
from collections import namedtuple
import functools
import importlib
import pprint

import kaitaistruct


FieldWithInfo = namedtuple(
    "FieldWithInfo", ("fieldname", "value", "offset", "length"))


class OffsetLookup(object):
    def __init__(self):
        self._offsets = {}
        self._lengths = {}
        self._fields_order = {}
        self._fieldnames = {}
        self._starts = []
        self._ends = []

    def offset(self, which, fieldname):
        return self._offsets[which][fieldname]

    def _check_object(self, which, fieldname):
        if which not in self._fields_order:
            self._fieldnames[which] = set()
            self._fields_order[which] = []
            self._offsets[which] = {}
            self._lengths[which] = {}
        if fieldname not in self._fieldnames[which]:
            self._fieldnames[which].add(fieldname)
            self._fields_order[which].append(fieldname)

    def set_offset(self, which, fieldname, value):
        self._check_object(which, fieldname)
        self._offsets[which][fieldname] = value

    def length(self, which, fieldname):
        return self._lengths[which][fieldname]

    def set_length(self, which, fieldname, value):
        self._check_object(which, fieldname)
        self._lengths[which][fieldname] = value

    def iter_fieldnames(self, which):
        return iter(self._fields_order[which])

    def set_start(self, start):
        self._starts.append(start)

    def set_end(self, end):
        self._ends.append(end)

    def pop_start_end(self):
        start = self._starts.pop()
        end = self._ends.pop()
        while self._starts and self._ends and (start, end) == (self._starts[-1], self._ends[-1]):
            self._starts.pop()
            self._ends.pop()
        return (start, end)


_LOOKUP = OffsetLookup()


def wrap_reader(method):
    @functools.wraps(method)
    def wrapper(self, *args, **kwargs):
        _LOOKUP.set_start(self.pos())
        value = method(self, *args, **kwargs)
        _LOOKUP.set_end(self.pos())
        return value
    return wrapper


def _get_start_and_end_of_kstruct(kstruct):
    start = None
    end = None
    for field in iter_fields_and_info(kstruct):
        if start is None or field.offset < start:
            start = field.offset
        if end is None or field.offset + field.length > end:
            end = field.offset + field.length
    return start, end


def _setit(self, name, value):
    self.__dict__[name] = value
    if name[0] != "_":
        if isinstance(value, kaitaistruct.KaitaiStruct):
            start, end = _get_start_and_end_of_kstruct(value)
        else:
            start, end = _LOOKUP.pop_start_end()
        _LOOKUP.set_offset(self, name, start)
        _LOOKUP.set_length(self, name, end - start)


def iter_fields_and_info(kstruct):
    for fieldname in _LOOKUP.iter_fieldnames(kstruct):
        yield FieldWithInfo(fieldname, getattr(kstruct, fieldname),
                            _LOOKUP.offset(kstruct, fieldname),
                            _LOOKUP.length(kstruct, fieldname))


def wrap_module(mod):
    try:
        mod = mod.kaitaistruct
    except AttributeError:
        pass
    mod.KaitaiStruct.__setattr__ = _setit
    mod.KaitaiStream.read_bytes = wrap_reader(
        mod.KaitaiStream.read_bytes)
    mod.KaitaiStream.read_bytes_full = wrap_reader(
        mod.KaitaiStream.read_bytes_full)
    mod.KaitaiStream.read_bytes_term = wrap_reader(
        mod.KaitaiStream.read_bytes_term)
    mod.KaitaiStream.read_f4be = wrap_reader(
        mod.KaitaiStream.read_f4be)
    mod.KaitaiStream.read_f4le = wrap_reader(
        mod.KaitaiStream.read_f4le)
    mod.KaitaiStream.read_f8be = wrap_reader(
        mod.KaitaiStream.read_f8le)
    mod.KaitaiStream.read_f8le = wrap_reader(
        mod.KaitaiStream.read_f8le)
    mod.KaitaiStream.read_s1 = wrap_reader(
        mod.KaitaiStream.read_s1)
    mod.KaitaiStream.read_s2be = wrap_reader(
        mod.KaitaiStream.read_s2be)
    mod.KaitaiStream.read_s2le = wrap_reader(
        mod.KaitaiStream.read_s2le)
    mod.KaitaiStream.read_s4be = wrap_reader(
        mod.KaitaiStream.read_s4be)
    mod.KaitaiStream.read_s8be = wrap_reader(
        mod.KaitaiStream.read_s8be)
    mod.KaitaiStream.read_s8le = wrap_reader(
        mod.KaitaiStream.read_s8le)
    mod.KaitaiStream.read_u1 = wrap_reader(
        mod.KaitaiStream.read_u1)
    mod.KaitaiStream.read_u2be = wrap_reader(
        mod.KaitaiStream.read_u2be)
    mod.KaitaiStream.read_u2le = wrap_reader(
        mod.KaitaiStream.read_u2le)
    mod.KaitaiStream.read_u4be = wrap_reader(
        mod.KaitaiStream.read_u4be)
    mod.KaitaiStream.read_u4le = wrap_reader(
        mod.KaitaiStream.read_u4le)
    mod.KaitaiStream.read_u8be = wrap_reader(
        mod.KaitaiStream.read_u8be)
    mod.KaitaiStream.read_u8le = wrap_reader(
        mod.KaitaiStream.read_u8le)
    mod.KaitaiStruct.isWrapped = True


def to_tree(kstruct):
    fields = []
    for field in iter_fields_and_info(kstruct):
        info = {'name': field.fieldname,
                'offset': field.offset,
                'length': field.length}
        if isinstance(field.value, kaitaistruct.KaitaiStruct):
            info['value'] = to_tree(field.value)
        else:
            info['value'] = field.value
        fields.append(info)
    return fields


def get_base_parser(modulefile):
    mod = importlib.import_module(modulefile)
    try:
        mod.KaitaiStruct.isWrapped
    except AttributeError:
        wrap_module(mod)
    assert mod.KaitaiStruct.isWrapped
    for name in dir(mod):
        obj = getattr(mod, name)
        if issubclass(obj, kaitaistruct.KaitaiStruct) and obj != kaitaistruct.KaitaiStruct:
            return obj
    return None


if __name__ == '__main__':
    import sys
    wrap_module(sys.modules['__main__'])
    import the_parser
    parsed = the_parser.TheParser.from_file("testfile")
    print(list(iter_fields_and_info(parsed)))
    pprint.pprint(to_tree(parsed))
    import type_parser
    parsed = type_parser.TypeParser.from_file("testfile")
    print(list(iter_fields_and_info(parsed)))
    print(list(iter_fields_and_info(parsed.the_type)))
    pprint.pprint(to_tree(parsed))

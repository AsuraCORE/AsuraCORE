"""Minimal readers/writers for modern (split) WoW ADT/WDT files - AsuraCORE map toolkit."""
import struct


def chunks(data, start=0, end=None):
    """Yield (tag, payload_offset, size) for a flat chunk list. Tags are returned readable (e.g. 'MCNK')."""
    p, end = start, len(data) if end is None else end
    while p + 8 <= end:
        tag = data[p:p + 4][::-1].decode('latin1')
        size = struct.unpack_from('<I', data, p + 4)[0]
        yield tag, p + 8, size
        p += 8 + size


def build(chunk_list):
    """chunk_list: [(tag, bytes)] -> file bytes."""
    out = bytearray()
    for tag, payload in chunk_list:
        out += tag.encode('latin1')[::-1] + struct.pack('<I', len(payload)) + payload
    return bytes(out)


def parse(data):
    return [(tag, data[o:o + s]) for tag, o, s in chunks(data)]


def terrain_heights(root):
    """Return list of (mcnk_index, base_z, min_h, max_h) from a root ADT."""
    res = []
    idx = 0
    for tag, o, s in chunks(root):
        if tag != 'MCNK':
            continue
        base_z = struct.unpack_from('<f', root, o + 0x68 + 8)[0]  # position[2] (MCNK header: position at 0x68)
        hs = None
        for st, so, ss in chunks(root, o + 0x80, o + s):
            if st == 'MCVT':
                hs = struct.unpack_from('<145f', root, so)
        if hs:
            res.append((idx, base_z, min(hs) + base_z, max(hs) + base_z))
        idx += 1
    return res


def texture_ids(tex0):
    for tag, o, s in chunks(tex0):
        if tag == 'MDID':
            return list(struct.unpack_from('<%dI' % (s // 4), tex0, o))
    return []

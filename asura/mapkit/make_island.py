"""
AsuraCORE map toolkit, stage 1: generate a brand-new map (not present in WoW) for the 12.1 client.

Output (F:/AsuraCORE/custom):
  files/world/maps/asurasanctum/*.wdt|*.adt   - terrain served to the client by the launcher
  mappings/asurasanctum.txt                    - fileDataId;path lines for the launcher
Template ADTs are empty flat tiles of Plunder Isle (map 1644), used only for their file layout.
"""
import math
import os
import struct

import adt

SRC = 'F:/AsuraCORE/client/casc-out/'
OUT = 'F:/AsuraCORE/custom/'
MAP_DIR = 'plunderisle'  # donor path in the listfile (the launcher replaces these FileDataIDs)

TEMPLATE_ROOT = 1439113   # PlunderIsle_29_29.adt (flat, empty)
TEMPLATE_OBJ0 = 1439116
TEMPLATE_OBJ1 = 1439119
DONOR_WDT = 1440315       # PlunderIsle.wdt (MPHD flags)
GROUND_TEXTURE = 5876849  # tileset/expansion11/12vdl_voidrockpattern01_1024.blp

# The launcher (Burralis) only replaces files that already exist in the client, it cannot add new
# FileDataIDs. So our map is delivered under the FileDataIDs of the unused Plunder Isle map (1644).
WDT_FDID = DONOR_WDT
TILES = [(29, 29), (30, 29), (29, 30), (30, 30)]  # (col, row) in the 64x64 grid

TILE = 1600.0 / 3.0       # 533.333
CHUNK = TILE / 16.0
UNIT = CHUNK / 8.0

CENTER = (1066.667, 1066.667)
PLATEAU_R = 330.0
CLIFF_W = 70.0
PLATEAU_Z = 40.0
ABYSS_Z = -140.0


def height(x, y):
    dx, dy = x - CENTER[0], y - CENTER[1]
    r = math.hypot(dx, dy)
    ang = math.atan2(dy, dx)
    # irregular coastline
    edge = PLATEAU_R + 35.0 * math.sin(3 * ang) + 20.0 * math.sin(7 * ang + 1.3)
    hills = 7.0 * math.sin(x / 45.0) * math.cos(y / 60.0) + 4.0 * math.sin((x + y) / 23.0)
    # central hill for the future sanctum
    hills += 18.0 * math.exp(-(r / 90.0) ** 2)
    top = PLATEAU_Z + hills
    if r <= edge:
        return top
    if r >= edge + CLIFF_W:
        return ABYSS_Z + 6.0 * math.sin(x / 30.0) * math.sin(y / 30.0)
    t = (r - edge) / CLIFF_W
    t = t * t * (3 - 2 * t)
    return top + (ABYSS_Z - top) * t


def vertex_positions(cx, cy):
    """145 (x, y) world positions of MCVT vertices for a chunk whose corner is (cx, cy)."""
    pos = []
    for row in range(17):
        if row % 2 == 0:
            for col in range(9):
                pos.append((cx - (row // 2) * UNIT, cy - col * UNIT))
        else:
            for col in range(8):
                pos.append((cx - (row // 2 + 0.5) * UNIT, cy - (col + 0.5) * UNIT))
    return pos


def normal(x, y):
    e = 1.0
    nx = height(x - e, y) - height(x + e, y)
    ny = height(x, y - e) - height(x, y + e)
    nz = 2.0 * e
    ln = math.sqrt(nx * nx + ny * ny + nz * nz)
    return nx / ln, ny / ln, nz / ln


def clamp_byte(v):
    return max(-127, min(127, int(round(v * 127))))


def make_root(template, tile_col, tile_row):
    base_x = (32 - tile_row) * TILE
    base_y = (32 - tile_col) * TILE
    out = []
    for tag, payload in adt.parse(template):
        if tag != 'MCNK':
            out.append((tag, payload))
            continue
        header = bytearray(payload[:0x80])
        ix, iy = struct.unpack_from('<II', header, 4)
        cx = base_x - iy * CHUNK
        cy = base_y - ix * CHUNK
        struct.pack_into('<I', header, 12, 1)                # nLayers
        struct.pack_into('<3f', header, 0x68, cx, cy, 0.0)   # position, heights are absolute
        verts = vertex_positions(cx, cy)
        subs = []
        for stag, spayload in adt.parse(payload[0x80:]):
            if stag == 'MCVT':
                spayload = struct.pack('<145f', *[height(x, y) for x, y in verts])
            elif stag == 'MCNR':
                nb = bytearray()
                for x, y in verts:
                    n = normal(x, y)
                    nb += struct.pack('<3b', clamp_byte(n[0]), clamp_byte(n[1]), clamp_byte(n[2]))
                spayload = bytes(nb) + spayload[435:]
            subs.append((stag, spayload))
        out.append(('MCNK', bytes(header) + adt.build(subs)))
    return adt.build(out)


def make_tex0():
    chunks = [('MVER', struct.pack('<I', 18)),
              ('MAMP', struct.pack('<I', 0)),
              ('MDID', struct.pack('<I', GROUND_TEXTURE)),
              ('MHID', struct.pack('<I', 0))]
    mcly = struct.pack('<4I', 0, 0, 0, 0)  # textureId, flags, offsetInMCAL, effectId
    for _ in range(256):
        chunks.append(('MCNK', adt.build([('MCLY', mcly)])))
    return adt.build(chunks)


def make_wdt(donor, tile_fdids):
    out = []
    for tag, payload in adt.parse(donor):
        # MPHD is kept as is: its flags promise lgt/occ/fogs/mpv/tex/wdl files and the client
        # raises a streaming error when those references are zero
        if tag == 'MAIN':
            main = bytearray(len(payload))
            for col, row in tile_fdids:
                o = (row * 64 + col) * 8
                main[o:o + 8] = payload[o:o + 8]
            payload = bytes(main)
        elif tag == 'MAID':
            maid = bytearray(len(payload))
            for (col, row), ids in tile_fdids.items():
                struct.pack_into('<8I', maid, (row * 64 + col) * 32, *ids)
            payload = bytes(maid)
        out.append((tag, payload))
    return adt.build(out)


def donor_tile_fdids(wdt):
    for tag, payload in adt.parse(wdt):
        if tag == 'MAID':
            ids = struct.unpack('<%dI' % (len(payload) // 4), payload)
            return {(i % 64, i // 64): ids[i * 8:i * 8 + 8] for i in range(4096) if ids[i * 8]}
    return {}


def main():
    read = lambda fdid: open(SRC + str(fdid), 'rb').read()
    files_dir = os.path.join(OUT, 'files', 'world', 'maps', MAP_DIR)
    os.makedirs(files_dir, exist_ok=True)
    os.makedirs(os.path.join(OUT, 'mappings'), exist_ok=True)

    mappings = []
    tile_fdids = {}
    donor_maid = donor_tile_fdids(read(DONOR_WDT))
    template_root, obj0, obj1 = read(TEMPLATE_ROOT), read(TEMPLATE_OBJ0), read(TEMPLATE_OBJ1)
    tex0 = make_tex0()
    for col, row in TILES:
        name = '%s_%d_%d' % (MAP_DIR, col, row)
        files = [(name + '.adt', make_root(template_root, col, row)),
                 (name + '_obj0.adt', obj0),
                 (name + '_obj1.adt', obj1),
                 (name + '_tex0.adt', tex0)]
        ids = donor_maid[(col, row)][:4]  # root, obj0, obj1, tex0 of the donor tile
        for fid, (fname, data) in zip(ids, files):
            open(os.path.join(files_dir, fname), 'wb').write(data)
            mappings.append('%d;world/maps/%s/%s' % (fid, MAP_DIR, fname))
        # root, obj0, obj1, tex0, lod, mapTexture, mapTextureN, minimap
        # lod, mapTexture, mapTextureN, minimap stay the donor's (the client requires them)
        tile_fdids[(col, row)] = list(ids) + list(donor_maid[(col, row)][4:8])

    wdt_name = MAP_DIR + '.wdt'
    open(os.path.join(files_dir, wdt_name), 'wb').write(make_wdt(read(DONOR_WDT), tile_fdids))
    mappings.insert(0, '%d;world/maps/%s/%s' % (WDT_FDID, MAP_DIR, wdt_name))

    open(os.path.join(OUT, 'mappings', MAP_DIR + '.txt'), 'w', newline='\n').write('\n'.join(mappings) + '\n')
    top = max(height(CENTER[0] + dx, CENTER[1] + dy) for dx in range(-20, 21, 5) for dy in range(-20, 21, 5))
    print('files:', len(mappings), 'WDT fdid', WDT_FDID, 'center', CENTER, 'center height %.1f' % top)


if __name__ == '__main__':
    main()

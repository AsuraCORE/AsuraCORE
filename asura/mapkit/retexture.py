"""
AsuraCORE map toolkit: re-skin an existing map by swapping its terrain textures (MDID/MHID in *_tex0.adt)
for a themed palette. Terrain shape and alpha maps stay as they are, so server terrain does not change.

  python retexture.py <wdt fdid> <map_dir> <tex0 source dir>

Writes F:/AsuraCORE/custom/files/world/maps/<map_dir>/*_tex0.adt; publish with
  python publish.py F:/AsuraCORE/custom/files <map_dir> 0 --client-only --deploy
"""
import os
import struct
import sys

import adt
import make_island

LISTFILE = 'F:/AsuraCORE/tools/listfile/community-listfile.csv'
OUT = 'F:/AsuraCORE/custom/files/'

# Void (Midnight) palette: first matching keyword wins.
VOID_PALETTE = [
    (('crystal',), 'tileset/expansion11/12vdl_crystalblue01_1024_s.blp'),
    (('lava', 'magma'), 'tileset/expansion11/12vdl_slimerock01_1024_s.blp'),
    (('sulfur', 'ash'), 'tileset/expansion11/12vdl_slimerock02_1024_s.blp'),
    (('grass', 'moss', 'root', 'leaf'), 'tileset/expansion11/12vdl_moss01_1024_s.blp'),
    (('tile', 'path', 'road', 'brick', 'floor'), 'tileset/expansion11/12vdl_road01_1024_s.blp'),
    (('sand',), 'tileset/expansion11/12vdl_sand01_512_s.blp'),
    (('stones', 'pebble', 'gravel', 'rubble'), 'tileset/expansion11/12vdl_stones01_512_s.blp'),
    (('dirt', 'mud', 'soil'), 'tileset/expansion11/12vdl_dirt01_1024_s.blp'),
    (('obsidian', 'volcanic', 'cracked'), 'tileset/expansion11/12vdl_voidrockpattern03_2048_s.blp'),
    (('bone', 'coin', 'gold'), 'tileset/expansion11/12vdl_voidrockpattern01_1024_s.blp'),
    (('rock', 'cliff', 'stone'), 'tileset/expansion11/12vdl_rock01_2048_s.blp'),
]
FALLBACK = 'tileset/expansion11/12vdl_voidrockpattern02_1024_s.blp'


def load_listfile():
    by_id, by_path = {}, {}
    with open(LISTFILE, encoding='utf-8') as f:
        for line in f:
            fid, _, path = line.rstrip('\n').partition(';')
            by_id[int(fid)] = path
            by_path[path] = int(fid)
    return by_id, by_path


def target_for(path):
    name = path.rsplit('/', 1)[-1]
    for keys, target in VOID_PALETTE:
        if any(k in name for k in keys):
            return target
    return FALLBACK


def height_texture(path, by_path):
    """Matching _h.blp for a *_s.blp diffuse, 0 if the client has none."""
    base = path[:-6] if path.endswith('_s.blp') else path[:-4]
    return by_path.get(base + '_h.blp', 0)


def retexture(data, by_id, by_path, used):
    out = []
    for tag, payload in adt.parse(data):
        if tag == 'MDID':
            ids = struct.unpack('<%dI' % (len(payload) // 4), payload)
            new = []
            for tid in ids:
                target = target_for(by_id.get(tid, ''))
                new.append(by_path[target])
                used[(by_id.get(tid, str(tid)), target)] = used.get((by_id.get(tid, str(tid)), target), 0) + 1
            mdid_targets = [by_id[i] for i in new]
            payload = struct.pack('<%dI' % len(new), *new)
        elif tag == 'MHID':
            payload = struct.pack('<%dI' % len(mdid_targets), *[height_texture(p, by_path) for p in mdid_targets])
        out.append((tag, payload))
    return adt.build(out)


def main():
    wdt_fdid, map_dir, src = int(sys.argv[1]), sys.argv[2], sys.argv[3]
    by_id, by_path = load_listfile()
    for _, target in VOID_PALETTE:
        assert target in by_path, target
    tiles = make_island.donor_tile_fdids(open(os.path.join(make_island.SRC, str(wdt_fdid)), 'rb').read())
    out_dir = OUT + 'world/maps/%s/' % map_dir
    os.makedirs(out_dir, exist_ok=True)
    used, count = {}, 0
    for ids in tiles.values():
        tex0 = ids[3]
        data = open(os.path.join(src, str(tex0)), 'rb').read()
        open(out_dir + by_id[tex0].rsplit('/', 1)[-1], 'wb').write(retexture(data, by_id, by_path, used))
        count += 1
    print('retextured %d tex0 files' % count)
    for (source, target), n in sorted(used.items(), key=lambda kv: -kv[1])[:12]:
        print('  %3d  %s -> %s' % (n, source.rsplit('/', 1)[-1], target.rsplit('/', 1)[-1]))


if __name__ == '__main__':
    main()

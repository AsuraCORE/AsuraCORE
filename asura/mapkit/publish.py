"""
AsuraCORE map toolkit: publish an edited map (split 12.1 ADT/WDT files, e.g. saved by AsuraNoggit)
to the client (Burralis custom files) and to the server (TrinityCore .map heights).

  python publish.py <source_root> <map_dir> <server_map_id> [--deploy] [--client-only]

  source_root   folder that contains world/maps/<map_dir>/ (a Noggit project folder or F:/AsuraCORE/custom/files)
  map_dir       e.g. plunderisle
  server_map_id Map.db2 ID the server uses for this terrain, e.g. 9000

FileDataIDs are resolved with tools/listfile/community-listfile.csv (the launcher can only replace existing IDs).
"""
import os
import re
import shutil
import struct
import subprocess
import sys

import adt
import server_map

ROOT = 'F:/AsuraCORE/'
LISTFILE = ROOT + 'tools/listfile/community-listfile.csv'
OUT_FILES = ROOT + 'custom/files/'
OUT_MAPPINGS = ROOT + 'custom/mappings/'
OUT_SERVER = ROOT + 'custom/server/maps/'
CLIENT_RETAIL = ROOT + 'client/World of Warcraft/_retail_/'
SERVER_MAPS = 'asura:/opt/asuracore/data/maps/'

TILE_RE = re.compile(r'_(\d+)_(\d+)(_obj0|_obj1|_tex0|_lod)?\.adt$')


def load_listfile(prefix):
    ids = {}
    with open(LISTFILE, encoding='utf-8') as f:
        for line in f:
            fid, _, path = line.rstrip('\n').partition(';')
            if path.startswith(prefix):
                ids[path] = int(fid)
    return ids


def root_heights(data):
    """V9 (129x129) and V8 (128x128) grids from a split root ADT; first index = world X."""
    v9 = [[0.0] * 129 for _ in range(129)]
    v8 = [[0.0] * 128 for _ in range(128)]
    for tag, o, s in adt.chunks(data):
        if tag != 'MCNK':
            continue
        ix, iy = struct.unpack_from('<II', data, o + 4)
        base_z = struct.unpack_from('<f', data, o + 0x68 + 8)[0]
        for st, so, ss in adt.chunks(data, o + 0x80, o + s):
            if st != 'MCVT':
                continue
            h = struct.unpack_from('<145f', data, so)
            k = 0
            for row in range(17):
                if row % 2 == 0:
                    for col in range(9):
                        v9[iy * 8 + row // 2][ix * 8 + col] = base_z + h[k]; k += 1
                else:
                    for col in range(8):
                        v8[iy * 8 + row // 2][ix * 8 + col] = base_z + h[k]; k += 1
    return [x for r in v9 for x in r], [x for r in v8 for x in r]


def server_map_file(data):
    v9, v8 = root_heights(data)
    area = b'AREA' + struct.pack('<HH', 0x1, 0)
    height = b'MHGT' + struct.pack('<Iff', 0, min(v9 + v8), max(v9 + v8))
    height += struct.pack('<16641f', *v9) + struct.pack('<16384f', *v8)
    area_off = 44
    header = b'MAPS' + struct.pack('<10I', server_map.MAP_VERSION_MAGIC, server_map.BUILD, area_off, len(area),
                                   area_off + len(area), len(height), 0, 0, 0, 0)
    return header + area + height


def main():
    args = [a for a in sys.argv[1:] if not a.startswith('--')]
    deploy = '--deploy' in sys.argv
    client_only = '--client-only' in sys.argv  # textures/objects only: keep server terrain untouched
    if len(args) != 3:
        print(__doc__)
        sys.exit(1)
    source_root, map_dir, map_id = args[0], args[1].lower(), int(args[2])
    rel_dir = 'world/maps/%s/' % map_dir
    src_dir = os.path.join(source_root, rel_dir)
    ids = load_listfile(rel_dir)

    mappings, tiles, missing = [], [], []
    os.makedirs(OUT_FILES + rel_dir, exist_ok=True)
    os.makedirs(OUT_SERVER, exist_ok=True)
    for name in sorted(os.listdir(src_dir)):
        path = rel_dir + name.lower()
        if not (name.endswith('.adt') or name.endswith('.wdt')):
            continue
        if path not in ids:
            missing.append(path)
            continue
        data = open(os.path.join(src_dir, name), 'rb').read()
        if os.path.abspath(os.path.join(src_dir, name)) != os.path.abspath(OUT_FILES + path):
            open(OUT_FILES + path, 'wb').write(data)
        mappings.append('%d;%s' % (ids[path], path))
        m = TILE_RE.search(name.lower())
        if m and not m.group(3) and not client_only:  # root ADT -> server heights
            col, row = int(m.group(1)), int(m.group(2))
            open(OUT_SERVER + '%04d_%02d_%02d.map' % (map_id, row, col), 'wb').write(server_map_file(data))
            tiles.append((col, row))

    if tiles:
        open(OUT_SERVER + '%04d.tilelist' % map_id, 'wb').write(server_map.tilelist(tiles))
    open(OUT_MAPPINGS + map_dir + '.txt', 'w', newline='\n').write('\n'.join(mappings) + '\n')
    print('client files: %d, server tiles: %d' % (len(mappings), len(tiles)))
    if missing:
        print('NOT IN LISTFILE (skipped, the launcher cannot add new FileDataIDs):', ', '.join(missing))

    if deploy:
        shutil.copytree(OUT_FILES + rel_dir, CLIENT_RETAIL + 'files/' + rel_dir, dirs_exist_ok=True)
        os.makedirs(CLIENT_RETAIL + 'mappings', exist_ok=True)
        shutil.copy(OUT_MAPPINGS + map_dir + '.txt', CLIENT_RETAIL + 'mappings/')
        if tiles:
            server_files = [OUT_SERVER + f for f in os.listdir(OUT_SERVER) if f.startswith('%04d' % map_id)]
            subprocess.run(['scp', '-q'] + server_files + [SERVER_MAPS], check=True)
            print('deployed to client and server (restart worldserver to reload terrain)')
        else:
            print('deployed to client (no server terrain changes)')


if __name__ == '__main__':
    main()

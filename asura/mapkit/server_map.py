"""
AsuraCORE map toolkit: write TrinityCore server terrain (.map + .tilelist) for a generated map,
from the same height function the client ADTs are built from (make_island.height).

Output: F:/AsuraCORE/custom/server/maps/{map:04}_{row:02}_{col:02}.map and {map:04}.tilelist
(upload to /opt/asuracore/data/maps).
"""
import os
import struct

import make_island as island

MAP_ID = 9000
BUILD = 69875
MAP_VERSION_MAGIC = 10
OUT = 'F:/AsuraCORE/custom/server/maps/'
RES = 128  # MAP_RESOLUTION


def grid(tile_col, tile_row, n, offset):
    """n x n heights; first index runs along world X (tile row), second along world Y (tile col)."""
    base_x = (32 - tile_row) * island.TILE
    base_y = (32 - tile_col) * island.TILE
    step = island.TILE / RES
    return [island.height(base_x - (i + offset) * step, base_y - (j + offset) * step)
            for i in range(n) for j in range(n)]


def map_file(tile_col, tile_row):
    v9 = grid(tile_col, tile_row, RES + 1, 0.0)
    v8 = grid(tile_col, tile_row, RES, 0.5)
    area = b'AREA' + struct.pack('<HH', 0x1, 0)                    # NoArea
    height = b'MHGT' + struct.pack('<Iff', 0, min(v9 + v8), max(v9 + v8))
    height += struct.pack('<%df' % len(v9), *v9) + struct.pack('<%df' % len(v8), *v8)
    header_size = 4 + 4 * 10
    area_off = header_size
    height_off = area_off + len(area)
    header = b'MAPS' + struct.pack('<10I', MAP_VERSION_MAGIC, BUILD, area_off, len(area), height_off, len(height), 0, 0, 0, 0)
    return header + area + height


def tilelist(tiles):
    bits = ['0'] * 4096
    for col, row in tiles:
        bits[4095 - (row * 64 + col)] = '1'  # std::bitset::to_string() order
    return b'MAPS' + struct.pack('<II', MAP_VERSION_MAGIC, BUILD) + ''.join(bits).encode()


def main():
    os.makedirs(OUT, exist_ok=True)
    for col, row in island.TILES:
        name = '%04d_%02d_%02d.map' % (MAP_ID, row, col)
        open(OUT + name, 'wb').write(map_file(col, row))
    open(OUT + '%04d.tilelist' % MAP_ID, 'wb').write(tilelist(island.TILES))
    c = island.CENTER
    print('server maps written for %d tiles; height at center %.1f' % (len(island.TILES), island.height(*c)))


if __name__ == '__main__':
    main()

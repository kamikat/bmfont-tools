#!/usr/bin/env python

from os import path

def rotate(line, dimen, r, s, num):
    bc = ((s * num + r) * dimen) % len(line)
    # print len(line), dimen, r, s, num, bc
    return line[-bc:] + line[:-bc]

if __name__ == '__main__':

    import argparse

    parser = argparse.ArgumentParser(description='Rotate pixels in tiled font data')
    parser.add_argument('dimension', type=int, help='Dimension of the tile (square)')
    parser.add_argument('linewidth', type=int, help='Number of tiles in a line')
    parser.add_argument('infile', help='Input raw bitmap font data')
    parser.add_argument('-o', '--outfile',
            default='font.bin',
            help='Output result to (default font.bin)')
    parser.add_argument('-b', '--bits',
            type=int, default=4, dest='bits',
            help='Bits per pixel in 4, 8, 16 and 32 (default 4)')
    parser.add_argument('-r', '--rotate', type=int, default=0,
            help='Tiles to move for each line')
    parser.add_argument('-s', '--step', type=int, default=0,
            help='Step between each rotate (default 0 tile)')

    args = parser.parse_args()

    # Check Tile Width Parameter

    filesz = path.getsize(args.infile)
    dimension = args.dimension
    width = args.linewidth

    if filesz % (dimension * (args.bits / 8.0)):
        print >>stderr, "Given width of tile does not compromise filesize"
        exit(-1)

    cnt_char = filesz / (dimension * dimension)

    if cnt_char % width:
        print >>stderr, "Given width of line does not compromise filesize"
        exit(-1)

    height = cnt_char / width

    BAND_BYTE = int(dimension * (args.bits / 8.0))
    LINE_WIDTH_BYTE = width * BAND_BYTE

    # Rotate each line of the bitmap

    f = open(args.infile, 'rb')
    o = open(args.outfile, 'wb')

    from itertools import count

    for i in count(0, 1):
        t = f.read(LINE_WIDTH_BYTE)
        if not t:
            break
        # Using byte dimension for tile
        o.write(rotate(t, BAND_BYTE, args.rotate, args.step, i))
    f.close()
    o.close()


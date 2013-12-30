#!/usr/bin/env python

from os import path

if __name__ == '__main__':

    import argparse

    parser = argparse.ArgumentParser(description='Flip Y coordinate of font data')
    parser.add_argument('dimension', type=int, help='Dimension of the tile (square)')
    parser.add_argument('linewidth', type=int, help='Number of tiles in a line')
    parser.add_argument('infile', help='Input raw bitmap font data')
    parser.add_argument('-o', '--outfile',
            default='flipy.bin',
            help='Output result to (default reverse.bin)')
    parser.add_argument('-b', '--bits',
            type=int, default=4, dest='bits',
            help='Bits per pixel in 4, 8, 16 and 32 (default 4)')

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

    stack = []

    while True:
        t = f.read(LINE_WIDTH_BYTE)
        if not t:
            break
        stack.append(t)

    while len(stack):
        o.write(stack.pop())

    f.close()
    o.close()


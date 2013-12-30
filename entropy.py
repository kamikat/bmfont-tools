#!/usr/bin/env python

from cStringIO import StringIO
from os import path
from sys import stderr, stdout

def entropy(data, width):
    entropy = 0
    height = len(data) / width
    for i in xrange(width):
        prev = None
        for j in xrange(height):
            pos = j * width + i
            t = data[pos: pos + 1]
            if t != prev:
                entropy += 1
                prev = t
    e1 = entropy
    entropy = 0
    height = len(data) / width
    for j in xrange(height):
        prev = None
        for i in xrange(width):
            pos = j * width + i
            t = data[pos: pos + 1]
            if t != prev:
                entropy += 1
                prev = t
    e2 = entropy
    return (e1 * e2) ** 0.5

if __name__ == '__main__':

    import argparse

    parser = argparse.ArgumentParser(description='Analyse possible dimension of tiled font data')
    parser.add_argument('dimension', type=int, help='Dimension of the tile (square)')
    parser.add_argument('infile', help='Input raw bitmap font data')
    parser.add_argument('-o', '--output',
            default='entropy.csv', dest='outfile',
            help='Output result to (default entropy.csv)')
    parser.add_argument('-b', '--bits',
            type=int, default=4, dest='bits',
            help='Bits per pixel in 4, 8, 16 and 32 (default 4)')

    args = parser.parse_args()

    # Check Tile Width Parameter

    filesz = path.getsize(args.infile)
    dimension = args.dimension

    if filesz % dimension:
        print >>stderr, "Given width of tile does not compromise filesize"
        exit(-1)

    print >>stderr, "Totally %d character tiles in bitmap." % (filesz / (args.bits / 8.0) / (dimension * dimension))

    # Read File

    data = open(args.infile, 'rb').read()

    # Tag Black/White Band

    print >>stderr, "Tagging bands..."

    BAND_DISTANCE = dimension * (args.bits / 4)
    BLACK_BAND = '0' * BAND_DISTANCE

    f = StringIO(data.encode('hex'))

    o = StringIO()

    cnt_black = cnt_white = 0

    while True:
        t = f.read(BAND_DISTANCE)
        if not t:
            break
        if t == BLACK_BAND:
            o.write(' ')
            cnt_black += 1
        else:
            o.write('%')
            cnt_white += 1

    f.close()

    sequence = o.getvalue()

    o.close()

    print >>stderr, "Get %d black and %d white bands" % (cnt_black, cnt_white)

    # Calculate entropy test result

    if args.outfile == '-':
        outfile = stdout
    else:
        outfile = open(args.outfile, 'w')

    print >>stderr, "Calculating entropy for each dimension..."

    SOLUTION_MAX=len(sequence) / dimension

    for i in xrange(1, SOLUTION_MAX):
        print >>outfile, '%d, %d' % (i, entropy(sequence, i))
        print >>stderr, '%d/%d solution tested\r' % (i, SOLUTION_MAX),
        if not i % 30:
            outfile.flush()


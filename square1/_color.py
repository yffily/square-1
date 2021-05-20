'''
Tools to perform color transformations on the virtual cube.
'''

from ._draw import *
from ._shape import *

# Find the index i such that f[i] starts opposite f[0].
def opposite_index(f):
    a = len(f[0])-1
    for i in range(1,len(f)):
        a += len(f[i])-1
        if a==6:
            return i+1
        if a>6:
            raise Exception('Forbiden twist (no face/slit alignment).')

# state = pair of faces
def twist(f1,f2):
    i1,i2 = opposite_index(f1),opposite_index(f2)
    x1 = f1[:i1] + f2[i2:]
    x2 = f2[:i2] + f1[i1:]
    return x1,x2

# # Example:
# draw(fu,fd)
# draw(*twist(fu,fd))

# Rotate a face by angle i*pi/6 cw.
def turn(f,i):
    i = i%12
    a = 0
    for j in range(len(f)):
        if a==i:
            return f[j:]+f[:j]
        if a>i:
            raise Exception('Forbiden turn (no face/slit alignment).')
        a += len(f[j])-1

# Parse a sequence from http://www.cubezone.be/square1.html. Return a
# function that takes a state, performs the sequence on it, and returns
# the result optionally drawing every intermediate step.
def parse_sequence(seq):
    seq = [m.strip() for m in seq.split(' ')]
    def perform_sequence(state, show_steps=False, seq=seq, **draw_options):
        f1,f2 = state
        for m in seq:
            if m=='/':
                f1,f2 = twist(f1,f2)
            else:
                i1,i2 = map(int,m[1:-1].split(','))
                f1,f2 = turn(f1,i1),turn(f2,i2)
            if show_steps:
                draw((f1,f2), **draw_options)
        return f1,f2
    return perform_sequence

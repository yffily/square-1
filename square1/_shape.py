'''
Tools to solve the shape of the cube, i.e., make it into an actual cube.
'''

from ._draw import *
import itertools

solved_cube = ( ('yg','ygo','yo','yob','yb','ybr','yr','yrg'), 
                ('wbo','wo','wog','wg','wgr','wr','wrb','wb') )

'''
Build the list of unique face shapes.
Map any face shape to an element of that list.
'''

# Check whether two shapes are identical up to a rotation.
def equal_up_to_rotation(f1,f2):
    if f1==f2:
        return True
    n = len(f1)
    if len(f2)!=n:
        return False
    for i in range(1,n):
        f1 = f1[1:] + f1[:1]
        if f1==f2:
            return True
    return False

# Generate all the possible shapes of a single face.
shapes = []
for f in [ (2,2,2,2,2,2), (2,2,2,2,2,1,1), (2,2,2,2,1,1,1,1), 
           (2,2,2,1,1,1,1,1,1), (2,2,1,1,1,1,1,1,1,1) ]:
    shapes += list(set(itertools.permutations(f,len(f))))

# Eliminate rotated duplicates to obtain the full list of unique face shapes.
# Make sure the solution (square shape) is at the beginning (useful to solve later).
shapes = [face2shape(solved_cube[0])] + shapes.copy()
n = 0
while n<len(shapes):
    shapes = shapes[:n+1] + [f for f in shapes[n+1:] if not equal_up_to_rotation(f,shapes[n])]
    n += 1

# Function to identify the unique shape a shape is homeomorphic to.
# Note: It could make sense to return the rotation angle as well.
def identify_shape(f,shapes=shapes):
    for f0 in shapes:
        if equal_up_to_rotation(f,f0):
            return tuple(f0)


'''
Build the list of unique physical pairs of shapes.
Map any pair of shapes to an element of that list.
'''

# Build list of pairs of physical faces.
shape_pairs = []
for f1 in shapes:
    for f2 in shapes:
        if f1.count(1)+f2.count(1)==8:
            shape_pairs.append((f1,f2))

# Function to identify the unique shape pair a shape pair is homeomorphic to.
def identify_pair(f1,f2):
    f1,f2 = tuple(f1),tuple(f2)
    x1,x2 = identify_shape(f1),identify_shape(f2)
    return x1,x2

# Functions to get the index of shapes in the `shapes` list.
def shape_id(f,shapes=shapes):
    return shapes.index(identify_shape(f))

def pair_id(f1,f2,shapes=shapes):
    return shapes.index(identify_shape(f1)),shapes.index(identify_shape(f2))

''' 
Simulate turning and twisting.
For each pair of shapes, build of list of every pair of shapes it 
can be transformed into with a single twist.
'''

# Turn a shape by i*pi/6.
def turn_shape(f,i):
    i = i%12
    a = 0
    for j in range(len(f)):
        if a==i:
            return f[j:]+f[:j]
        if a>i:
            return None
#             raise Exception('Forbiden turn (no face/slit alignment).')
        a += f[j]

# Find the index of the opposite side, if it exists.
# Return None if the slit is covered by a large wedge preventing twisting.
def twist_index(f):
    a = f[0]
    for i in range(1,len(f)):
        a += f[i]
        if a==6:
            return i+1
        if a>6:
            return None

def twist_shape(x1,x2,i1=None,i2=None):
    if i1==None:
        i1 = twist_index(x1)
    if i2==None:
        i2 = twist_index(x2)
    if i1==None or i2==None:
        return None
    x1,x2 = tuple(x1[:i1]+x2[i2:]),tuple(x2[:i2]+x1[i1:])
    return x1,x2
        
# For each pair of shapes, build a set of all the pairs of shapes it can be
# transformed into with turns and a single twist.
transition_dict = {}
for f1,f2 in shape_pairs:
    transition_dict[(f1,f2)] = []
    reachable_pairs = {(f1,f2)}
    for i1 in range(12):
        x1 = turn_shape(f1,i1)
        if x1==None:
            continue
        j1 = twist_index(x1)
        if j1==None:
            continue
        for i2 in range(12):
            x2 = turn_shape(f2,i2)
            if x2==None:
                continue
            j2 = twist_index(x2)
            if j2==None:
                continue
            # Perform twist.
            y1,y2 = tuple(x1[:j1]+x2[j2:]),tuple(x2[:j2]+x1[j1:])
            y1,y2 = identify_shape(y1),identify_shape(y2)
            if (y1,y2) not in reachable_pairs:
                reachable_pairs.add((y1,y2))
                transition_dict[(f1,f2)].append((y1,y2,i1,i2))

'''
Build solution paths by "concentric rings". The zeroth ring is the solved state. 
The first ring consists of the states with a transition to the solved state.
Ring n consists of the states with a transition to a state in ring n-1.
Each object in a ring is a path to the solved state as a list of (state,transition)
objects where the state is a pair of faces and the transition is a pair of splits 
(one for each face, each split is a pair of halves). 
'''

# Function to identify the turns needed for a transition.
# This is needed because the solution was constructed backwards, starting
# from the solved state and working back to the initial state. To get the 
# correct turns and twists needed to go from the initial state to the solved
# state we need to construct the reverse of every transition.
def find_twist(p1,p2,transition_dict=transition_dict):
    for t in transition_dict[p1]:
        if p2==t[:2]:
            return t[2:]

_remaining_confs = shape_pairs[1:].copy()
solution_rings = [ [ [ [shape_pairs[0],[0,0]] ] ] ]
while len(_remaining_confs)>0:
    new_ring = []
    for path in solution_rings[-1]:
        p2 = path[0][0]
        for t in transition_dict[p2]:
            p1 = t[:2]
            if p1 in _remaining_confs:
                i1,i2 = find_twist(p1,p2)
                new_ring.append([[p1,(i1,i2)]]+path)
                _remaining_confs.remove(p1)
    solution_rings.append(new_ring)

# Convert the list of rings of solutions to a dictionary of solutions.
# Given a pair p, solution_dict[p] is the path to the solution as a list
# of (pair,splits) objects.
solution_dict = { path[0][0]:path for path in sum(solution_rings,[]) }

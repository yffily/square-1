'''
Tools to draw the cube.
'''

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon


# Define the faces of the solved cube (upper face, then lower face)
solved_cube = ( ('yg','ygo','yo','yob','yb','ybr','yr','yrg'), 
                ('wbo','wo','wog','wg','wgr','wr','wrb','wb') )

# Rotate point(s) `xy` by `angle` around the origin.
def rotate(xy, angle, axis=0):
    c,s = np.cos(angle),np.sin(angle)
    return np.array([c*xy[0]-s*xy[1], s*xy[0]+c*xy[1]])

# Generate the xy coordinates of the corners of a small wedge and a large wedge.
xy = [ np.array([[0,0], [1,-np.sin(np.pi/12)], [1,np.sin(np.pi/12)], [0,0]]),
       np.array([[0,0], [1,np.sin(np.pi/12)], [1,1],[np.sin(np.pi/12),1], [0,0]]) ]
# Rotate them ccw so they start on x axis.
xy = [ rotate(xy[0].T,np.pi/12).T, rotate(xy[1].T,-np.pi/12).T ]

# Draw a wedge.
# `angle` is measured from the +x axis.
def draw_wedge(colors='wrb', angle=0, origin=[0,0], ax=None, xy=xy):
    if ax==None:
        ax = plt.gca()
    origin = np.array(origin)
    xy = 0.5*xy[len(colors)-2].T
    xy = rotate(xy, angle).T + origin[None,:]
    ax.add_patch(Polygon(xy, fc=colors[0], alpha=0.5))
    ax.plot(*xy[[-2,-1,1]].T, color='k',lw=1)
    for i in range(1,len(colors)):
        c  = (1,0.5,0) if colors[i]=='o' else colors[i]
        ax.plot(*xy[i:i+2].T, color=c, lw=4)
    # Return polar angle of furthest ccw edge (where the next wedge starts).
    return angle+(len(colors)-1)*np.pi/6

# Draw a line corresponding to a valid swap of halves at angle `angle`.
# `angle` is measured from the +x axis.
def draw_slit(angle=None, origin=[0,0], ax=None):
    if angle!=None:
        if ax==None:
            ax = plt.gca()
        x0,y0 = origin
        x,y   = 0.9*np.array([np.cos(angle),np.sin(angle)])
        ax.plot([x0-x,x0+x], [y0-y,y0+y], color='m', lw=3)
    return

# Draw the state of the cube (upper and lower face), plus optional swap lines.
# f1 = top face
# f2 = bottom face
# slit = angle between the +x axis and the slit in each face. 'None' means no slit.
# face_separation = horizontal distance between the two faces
slit1 = (np.pi/2,np.pi/2) # vertical slits
slit2 = (5*np.pi/12,7*np.pi/12) # horizontal/vertical face edges
def draw(state, slit=slit2, face_separation=2):
    f1,f2 = state
    fig = plt.figure(figsize=(6,2.5))
    ax  = fig.add_axes([0,0,1,1])
    if slit!=None:
        draw_slit(slit[0])
        draw_slit(slit[1], origin=[face_separation,0])
    else:
        slit = slit2
    angle = slit[0]
    for i,w in enumerate(f1):
        angle = draw_wedge(colors=w, angle=angle)
    angle = slit[1]
    for i,w in enumerate(f2):
        angle = draw_wedge(colors=w, angle=angle, origin=[face_separation,0])
    plt.axis('off')
    w,h = fig.get_size_inches()
    plt.xlim(-1,3)
    plt.ylim(-2*h/w,2*h/w)
    plt.show()    


# Convert a face object (shape+color information) to a shape object (no color information).
def face2shape(f):
    return tuple(len(w)-1 for w in f)

# Draw the shape state of the cube given its two faces as shapes objects.
def draw_shape(shape, slit=slit2, **args):
    s1,s2 = shape
    f1 = [ 'wkk' if w==2 else 'wk' for w in s1 ]
    f2 = [ 'wkk' if w==2 else 'wk' for w in s2 ]
    draw((f1,f2), slit=slit, **args)



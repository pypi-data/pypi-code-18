import numpy
# From: https://stackoverflow.com/questions/14177744/how-does-perspective-transformation-work-in-pil

def find_coeffs(pa, pb):
    """
    pa and pb contain 4 corresponding points on image in order UL,UR,LR,LL
    UL=(0,0), UR=(w,0), LR=(w,h), LL=(0,h)
    
    Units for pa and pb are pixels.
    pa is target plane (e.g. [(0, 0), (256, 0), (256, 256), (0, 256)])
    pb is source plane (e.g. [(0, 0), (256, 0), (new_width, height), (xshift, height)])
    """
    matrix = []
    for p1, p2 in zip(pa, pb):
        matrix.append([p1[0], p1[1], 1, 0, 0, 0, -p2[0]*p1[0], -p2[0]*p1[1]])
        matrix.append([0, 0, 0, p1[0], p1[1], 1, -p2[1]*p1[0], -p2[1]*p1[1]])

    A = numpy.matrix(matrix, dtype=numpy.float)
    B = numpy.array(pb).reshape(8)

    #res = numpy.dot(numpy.linalg.inv(A.T * A) * A.T, B)
    # take commenters advice to avoid A.T
    res = numpy.linalg.solve(A, B)
    return numpy.array(res).reshape(8)

def fix_plot_img( pos_xmin, pos_xmax, pos_ymin, pos_ymax, img):
    """
    Correct plot so that xmin and xmax have same y value.
    And, ymin/ymax have same x value
    """
    xlo = pos_xmin[0]
    xhi = pox_xmax[0]
    
    # Note y reversed because 0,0 is UL
    ylo = pos_ymin[1]
    yhi = pos_ymax[1]
    
    # make target points
    UL = (xlo, yhi)
    UR = (xhi, yhi)
    LR = (xhi, ylo)
    LL = (xlo, ylo)
    pa = [UL,UR,LR,LL]
    
    # make source points
    dxlo = pos_ymax[0] - pos_ymin[0]
    dylo = pos_xmax[1] - pos_xmin[1]
    UL = (xlo+dxlo, yhi)
    LR = (xhi, ylo+dylo)
    pb = [UL,UR,LR,LL]
    
    coeffs = find_coeffs(pa, pb)
    img.transform((width, height), Image.PERSPECTIVE, coeffs, Image.BICUBIC)
    
    
    
    
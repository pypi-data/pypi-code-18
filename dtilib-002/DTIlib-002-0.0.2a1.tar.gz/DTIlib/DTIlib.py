
# coding: utf-8

# # DTIlib

# Library to manipulate DTI data.

# ### All functions need the input data to be the folowing fomat
# 
# Scalar volume = [z,y,x]
# 
# evl = [evl1] [evl2] [evl3]
# 
# evt = [evt(1, 2, 3)] [componentes dos evt (z, y, x)] [Z] [Y] [X]

# In[ ]:

def load_fa_evl_evt(BASE_PATH):
    import nibabel as ni #pip install nibabel
    import numpy as np

    #-------------------------------------------------------
    FA_PATH = "%s%s" % ( BASE_PATH, '/dti_FA.nii.gz' )

    L1_PATH = "%s%s" % ( BASE_PATH, '/dti_L1.nii.gz' )
    L2_PATH = "%s%s" % ( BASE_PATH, '/dti_L2.nii.gz' )
    L3_PATH = "%s%s" % ( BASE_PATH, '/dti_L3.nii.gz' )

    V1_PATH = "%s%s" % ( BASE_PATH, '/dti_V1.nii.gz' )
    V2_PATH = "%s%s" % ( BASE_PATH, '/dti_V2.nii.gz' )
    V3_PATH = "%s%s" % ( BASE_PATH, '/dti_V3.nii.gz' )
    #-------------------------------------------------------
    FA = ni.load(FA_PATH).get_data()
#     print('FA Loaded')

    L1 = ni.load(L1_PATH).get_data()
    L2 = ni.load(L2_PATH).get_data()
    L3 = ni.load(L3_PATH).get_data()
#     print('EVL Loaded')

    V1 = ni.load(V1_PATH).get_data()
    V2 = ni.load(V2_PATH).get_data()
    V3 = ni.load(V3_PATH).get_data()
#     print('EVT Loaded')
    #-------------------------------------------------------
    fa = np.swapaxes(FA,0,2)

    l1 = np.swapaxes(L1,0,2)

    l2 = np.swapaxes(L2,0,2)

    l3 = np.swapaxes(L3,0,2)
    #-------------------------------------------------------
    v1 = np.swapaxes(V1,0,3)
    v1 = np.swapaxes(v1,1,2)
    v1[:,:,:,:] = v1[::-1,:,:,:]

    v2 = np.swapaxes(V2,0,3)
    v2 = np.swapaxes(v2,1,2)
    v2[:,:,:,:] = v2[::-1,:,:,:]

    v3 = np.swapaxes(V3,0,3)
    v3 = np.swapaxes(v3,1,2)
    #-------------------------------------------------------

    evl = np.array([l1,l2,l3])
    evt = np.array([v1,v2,v3])


    return fa, evl, evt


# ### Manipulação de volumes (rotações)

# In[1]:

#rotaciona vetores
def rot_vec(vec, angle = 90, axis = 'z'):
     
    angle = angle*np.pi/180

    if (axis == 'x'):
        rot = np.array([[np.cos(angle), -np.sin(angle), 0], [np.sin(angle), np.cos(angle), 0], [0, 0, 1]])
   
    if (axis == 'y'):
        rot = np.array([[np.cos(angle), 0, np.sin(angle)], [0, 1, 0], [-np.sin(angle), 0, np.cos(angle)]])

    if (axis == 'z'):
        rot = np.array([[1, 0, 0], [0, np.cos(angle), -np.sin(angle)], [0, np.sin(angle), np.cos(angle)]])
        
    print rot
    
    vec_rot = np.dot(vec,rot)
    
    return vec_rot

#rotaciona vetores dentro do voxel / antigo rotEVT
def rot_local_3vec(evt, angle = 90, axis = 'z'):
     
    angle = angle*np.pi/180

    if (axis == 'x'):
        rot = np.array([[np.cos(angle), -np.sin(angle), 0], [np.sin(angle), np.cos(angle), 0], [0, 0, 1]])
   
    if (axis == 'y'):
        rot = np.array([[np.cos(angle), 0, np.sin(angle)], [0, 1, 0], [-np.sin(angle), 0, np.cos(angle)]])

    if (axis == 'z'):
        rot = np.array([[1, 0, 0], [0, np.cos(angle), -np.sin(angle)], [0, np.sin(angle), np.cos(angle)]])
    
    evt_aux = np.swapaxes(evt,1,4)
    evt_rot = np.dot(evt_aux,rot)
    evt_rot = np.swapaxes(evt_rot,1,4)
    
    return evt_rot


#rotaciona Volumes
def rot_vol(vol, angle = 90, axis = 'z', int_order = 0, reshape=True, cval=0.0):
    import numpy as np
    import scipy.ndimage.interpolation as sni

    if (axis == 'z'):
        a = 0
        b = 2
    if (axis == 'y'):
        a = 1
        b = 2
    if (axis == 'x'):
        a = 0
        b = 1
    
    vol = np.swapaxes(vol,a,b)
    vol_r = sni.rotate(vol, angle, axes=(1, 0), reshape=reshape, output=None, order=int_order, mode='constant', cval=cval, prefilter=True)
    vol_r = np.swapaxes(vol_r,a,b)
    
    return vol_r

#rotaciona os vetores de um voxel para outro (translada os vetores)
def rot_external_3vec(evt, angle = 90, axis = 'z', int_order = 0, reshape=True, cval=0.0):
    import numpy as np
    
    evt00_r = rot_vol(evt[0,0,:,:,:], angle = angle, axis = axis, int_order = int_order, reshape=reshape, cval=cval)
    evt01_r = rot_vol(evt[0,1,:,:,:], angle = angle, axis = axis, int_order = int_order, reshape=reshape, cval=cval)
    evt02_r = rot_vol(evt[0,2,:,:,:], angle = angle, axis = axis, int_order = int_order, reshape=reshape, cval=cval)

    evt10_r = rot_vol(evt[1,0,:,:,:], angle = angle, axis = axis, int_order = int_order, reshape=reshape, cval=cval)
    evt11_r = rot_vol(evt[1,1,:,:,:], angle = angle, axis = axis, int_order = int_order, reshape=reshape, cval=cval)
    evt12_r = rot_vol(evt[1,2,:,:,:], angle = angle, axis = axis, int_order = int_order, reshape=reshape, cval=cval)

    evt20_r = rot_vol(evt[2,0,:,:,:], angle = angle, axis = axis, int_order = int_order, reshape=reshape, cval=cval)
    evt21_r = rot_vol(evt[2,1,:,:,:], angle = angle, axis = axis, int_order = int_order, reshape=reshape, cval=cval)
    evt22_r = rot_vol(evt[2,2,:,:,:], angle = angle, axis = axis, int_order = int_order, reshape=reshape, cval=cval)
                    
    z, y, x = evt00_r.shape
    evt_r = np.zeros((3,3,z,y,x))
                          
    evt_r[0,0] = evt00_r
    evt_r[0,1] = evt01_r
    evt_r[0,2] = evt02_r

    evt_r[1,0] = evt10_r
    evt_r[1,1] = evt11_r
    evt_r[1,2] = evt12_r

    evt_r[2,0] = evt20_r
    evt_r[2,1] = evt21_r
    evt_r[2,2] = evt22_r
    
    return evt_r

#rotaciona os autovalores (translada)
def rot_evl(evl, angle = 90, axis = 'z', int_order = 0, reshape=True, cval=0.0):
    import numpy as np
    
    evl0_r = rot_vol(evl[0,:,:,:], angle = angle, axis = axis, int_order = int_order, reshape=reshape, cval=cval)
    evl1_r = rot_vol(evl[1,:,:,:], angle = angle, axis = axis, int_order = int_order, reshape=reshape, cval=cval)
    evl2_r = rot_vol(evl[2,:,:,:], angle = angle, axis = axis, int_order = int_order, reshape=reshape, cval=cval)

    z, y, x = evl0_r.shape
    evl_r = np.zeros((3,z,y,x))
                          
    evl_r[0] = evl0_r
    evl_r[1] = evl1_r
    evl_r[2] = evl2_r

    return evl_r

#rotaciona completamente 3 campos vetoriais (formato de evt)
def rot_3VF(VFs, angle = 90, axis = 'z', int_order = 0, reshape=True, cval=0.0):
    import numpy as np
    
    VFs = rot_local_3vec(VFs, angle = angle, axis = axis)
    
    VFs_rot = rot_external_3vec(VFs, angle = angle, axis = axis, int_order = int_order, reshape=reshape, cval=cval)
    
    return VFs_rot


#rotaciona EVT * EVL (esse fica bom para interpolar)
def rot_evt_evl(evt, evl, angle = 90, axis = 'z', int_order = 3, reshape=True, cval=0.0):
    import numpy as np
    
    aux = evl*np.swapaxes(evt,0,1)
    evtl = np.swapaxes(aux,0,1)
    
    evtl_rot = rot_3VF(evtl, angle = angle, axis = axis, int_order = int_order, reshape=reshape, cval=cval)
    evl_rot = rot_evl(evl, angle = angle, axis = axis, int_order = int_order, reshape=reshape, cval=cval) + 0.000000000000000000001
    
    aux = np.swapaxes(evtl_rot,0,1)/evl_rot #encontro os autovetores novamente (acredito que ainda é só uma aproximação)
    evt_rot = np.swapaxes(aux,0,1)
    
    return evt_rot, evl_rot

#rotaciona EVT * EVL (esse fica bom para interpolar) (acho que essa é a certa)
def rot_evt_evl_2(evt, evl, angle = 90, axis = 'z', int_order = 3, reshape=True, cval=0.0):
    import numpy as np
    
    aux = evl*np.swapaxes(evt,0,1)
    evtl = np.swapaxes(aux,0,1)
    
    evtl_rot = rot_3VF(evtl, angle = angle, axis = axis, int_order = int_order, reshape=reshape, cval=cval)
    
    evl_new = np.linalg.norm(evtl_rot, axis=1) + 0.000000000000000000001
    aux = np.swapaxes(evtl_rot,0,1)/evl_new #acho que agora está certo
    evt_rot = np.swapaxes(aux,0,1)
    
    return evt_rot, evl_new


#rotaciona EVT, EVL e FA
def rot_evt_evl_fa(evt, evl, fa, angle = 90, axis = 'z', int_order = 3, reshape=True, cval=0.0):
    import numpy as np
    
    evt_rot, evl_rot = rot_evt_evl_2(evt, evl, angle=angle, axis=axis, int_order=int_order, reshape=reshape, cval=cval)
    fa_rot = rot_vol(fa, angle=angle, axis=axis, int_order=int_order, reshape=reshape, cval=cval)
    
    return evt_rot, evl_rot, fa_rot


# Duplica a resolução em Z
def interpola_Z(evt, evl, fa):
    import numpy as np
    
    aux1 = evl*np.swapaxes(evt,0,1)
    evtl = np.swapaxes(aux1,0,1)

    _, _, sz, sy, sx = evtl.shape

    evtl_interpolated = np.zeros((3, 3, sz*2 - 1, sy, sx))
    fa_interpolated = np.zeros((sz*2 - 1, sy, sx))


    fa_interpolated[::2] = fa
    fa_interpolated[1:-1:2] = (fa[1:] + fa[:-1])/2

    evtl_interpolated[:,:,::2] = evtl
    evtl_interpolated[:,:,1:-1:2] = (evtl[:,:,1:] + evtl[:,:,:-1])/2


    evl_new = np.linalg.norm(evtl_interpolated, axis=1) + 0.000000000000000000001
    aux = np.swapaxes(evtl_interpolated,0,1)/evl_new #acho que agora está certo
    evt_interpolated = np.swapaxes(aux,0,1)
    
    return evt_interpolated, evl_new, fa_interpolated

# Duplica a resolução em Z
def interpola_Z_2(evt, evl, fa):
    import numpy as np
    
    aux1 = evl*np.swapaxes(evt,0,1)
    evtl = np.swapaxes(aux1,0,1)

    _, _, sz, sy, sx = evtl.shape

    evtl_interpolated = np.zeros((3, 3, sz*2, sy, sx))
    fa_interpolated = np.zeros((sz*2, sy, sx))


    fa_interpolated[::2] = fa
    fa_interpolated[1::2] = fa

    evtl_interpolated[:,:,::2] = evtl
    evtl_interpolated[:,:,1::2] = evtl


    evl_new = np.linalg.norm(evtl_interpolated, axis=1) + 0.000000000000000000001
    aux = np.swapaxes(evtl_interpolated,0,1)/evl_new #acho que agora está certo
    evt_interpolated = np.swapaxes(aux,0,1)
    
    return evt_interpolated, evl_new, fa_interpolated


# # DTI measurements

# In[ ]:

#MD
def Mean_Difusivity(evl):
    import numpy as np
    
    MD = np.sum(evl,axis=0)/3
    
    return MD

def getFractionalAnisotropy(eigvals):
    import numpy as np
    MD = eigvals.mean(axis=0)
    FA = np.sqrt(3*((eigvals-MD)**2).sum(axis=0)) / np.sqrt(2*(eigvals**2).sum(axis=0))
    
    return (FA,MD)


# # Vector field manipulation

# In[1]:

# Cria a imagem de um campo vetorial 2d
def show_vector_field(y, x, step=32, maxlen=24, rescale=1, showPoints=False, color=(0,0,255), bgcolor=(255,255,255), pointsColor=(255,0,0), precision=3):
    import numpy as np
    # importopenCV
    import cv2
    
    H, W = x.shape
    img = np.array(bgcolor, np.uint8).reshape((1,1,3)) * np.ones((rescale*H, rescale*W, 3), np.uint8)
    #mask_y, mask_x = np.mgrid[step/2 : H : step, step/2 : W : step]
    mask_y, mask_x = np.mgrid[int(step/2) : int(H) : int(step), int(step/2) : int(W) : int(step)]
#     print(mask_y.shape)
#     print(mask_x.shape)
    ssx = x[mask_y, mask_x]
    ssy = y[mask_y, mask_x]
    mag = np.sqrt(ssx**2+ssy**2)
    magmax = np.max(mag)
    cx = ssx / (magmax+0.0000000000000000001)
    cy = ssy / (magmax+0.0000000000000000001)
    dx = ssx / (mag+0.0000000000000000001)
    dy = ssy / (mag+0.0000000000000000001)
    dx[np.isnan(dx)] = 0
    dy[np.isnan(dy)] = 0
    p = 2**precision
    pt1_x = (p*(rescale*mask_x - 0.5*maxlen*cx)).astype(int)
    pt1_y = (p*(rescale*mask_y - 0.5*maxlen*cy)).astype(int)
    pt2_x = (p*(rescale*mask_x + 0.5*maxlen*cx)).astype(int)
    pt2_y = (p*(rescale*mask_y + 0.5*maxlen*cy)).astype(int)
    pt3_x = ((pt2_x - p*maxlen*(0.2*dx-0.1*dy))).astype(int)
    pt3_y = ((pt2_y - p*maxlen*(0.2*dy+0.1*dx))).astype(int)
    pt4_x = ((pt2_x - p*maxlen*(0.2*dx+0.1*dy))).astype(int)
    pt4_y = ((pt2_y - p*maxlen*(0.2*dy-0.1*dx))).astype(int)
    for i in np.arange(mask_y.shape[0]):
        for j in np.arange(mask_x.shape[1]):
            cv2.line(img, (pt1_x[i,j], pt1_y[i,j]), (pt2_x[i,j], pt2_y[i,j]), color, lineType=8, shift=precision)
            cv2.line(img, (pt2_x[i,j], pt2_y[i,j]), (pt3_x[i,j], pt3_y[i,j]), color, lineType=8, shift=precision)
            cv2.line(img, (pt2_x[i,j], pt2_y[i,j]), (pt4_x[i,j], pt4_y[i,j]), color, lineType=8, shift=precision)

    if showPoints:
        from scipy.ndimage.measurements import minimum_position
        mag2 = x**2+y**2
        min_pos = minimum_position(mag2)
        if type(min_pos) == tuple:
            min_pos = [min_pos]
        for i,j in min_pos:
            cv2.circle(img, (rescale*j, rescale*i), 3, pointsColor, thickness=-1)

    img = np.swapaxes(np.swapaxes(img,0,2),1,2)

    return img


def set_direction(v, direction): # Coloca uma direção de interesse em um campo vetorial 3d
    import numpy as np
    direction = direction.reshape(3,1,1,1)
    dot_product = np.sum(direction*v, axis=0)
    s = np.sign(dot_product)
    s[s==0] = 1
    return s*v


def set_directions(v, directions): # Coloca várias direções de interesse em um campo vetorial 3d
    import numpy as np
    nd = directions.size/3
    directions = directions.reshape(nd,3,1,1,1)
    dot_product = np.sum(directions*v, axis=1)
    s = np.sign(dot_product)
    s[s==0] = 1
    
    nv, x, y, z = v.shape
    S = np.zeros((nd,3,x,y,z))

    S = v.reshape(1,3,x,y,z)*s.reshape(nd,1,x,y,z)
    
    return S

#Directions os Study for plane fittiong
#Calculas as direções de interesse dado o angulo minimo e o intervalo entre angulos. O resultado é um cone semi-esférico do angulo mínimo até 90
# angulos float
def calcdirections4(d = 1.0, min_angle=70):
    import numpy as np

    angles = np.asarray(np.arange(min_angle, 181 - min_angle, d))
    angles_rad = angles*np.pi/180

    z = np.sin(angles_rad)
    x = np.cos(angles_rad)

    Directions = np.array([z, np.zeros(z.size),x])
    Directions[np.absolute(Directions)<0.001] = 0
    na = angles.size

    return na, Directions.T


# # Synthetic data

# In[ ]:

#cria o TORUS (evl1 = l1, evl2 = l2, evl3 = l3)
def Torus(l1, l2, l3, n, R, r):
    import numpy as np

    centro = (n-1.)/2

    z,y,x = np.mgrid[0:n,0:n,0:n] 
    t = np.zeros(x.shape)
    t = (((R-(((x-centro)**2)+((y-centro)**2))**0.5)**2+(z-centro)**2-r**2)<0)

    # Calcula autovalores
    eigvals = np.ones(np.append(3,t.shape))
    eigvals[0] *= l1
    eigvals[1] *= l2
    eigvals[2] *= l3

    # Inicializa os autovetores do background
    eigvectsback = np.zeros(np.append((3,3),t.shape))
#     print('eigvectsback.shape = ', eigvectsback.shape)
    eigvectsback[0,0] = np.ones(t.shape)
    eigvectsback[1,1] = np.ones(t.shape)
    eigvectsback[2,2] = np.ones(t.shape)

    # Inicializa os autovetores do torus
    eigvectstorus = np.zeros(np.append((3,3),t.shape))
    eigvectstorus[2,0] = -np.ones(t.shape)

    # Modifica os autovetores pertencentes ao torus, tornando-os tangente 
    # à superficie do torus
    temp1 = (centro-y)/((centro-x)**2+(centro-y)**2)**0.5
    temp2 = (x-centro)/((centro-x)**2+(centro-y)**2)**0.5
    temp1[np.nonzero(np.isnan(temp1))] = 0
    temp2[np.nonzero(np.isnan(temp2))] = 0
    eigvectstorus[0,2] = temp1
    eigvectstorus[0,1] = temp2

    eigvectstorus[1,2] = temp2
    eigvectstorus[1,1] = -temp1

    # Calcula os autovetores para a imagem toda (combinando background+torus)
    eigvects = eigvectsback*(1-t)+eigvectstorus*t

    return eigvals,eigvects




#cria o kissing
def kissing(l1, l2, l3, n, R, r):
    import numpy as np

    centro = (n-1.)/2

    z,y,x = np.mgrid[0:n,0:n,0:n] 
    t = np.zeros(x.shape)
    t = (((R-(((x-centro)**2)+((y-centro)**2))**0.5)**2+(z-centro)**2-r**2)<0)

    # Calcula autovalores
    eigvals = np.ones(np.append(3,t.shape))
    eigvals[0] *= l1
    eigvals[1] *= l2
    eigvals[2] *= l3

    # Inicializa os autovetores do background
    eigvectsback = np.zeros(np.append((3,3),t.shape))
#     print('eigvectsback.shape = ', eigvectsback.shape)
    eigvectsback[0,0] = np.ones(t.shape)
    eigvectsback[1,1] = np.ones(t.shape)
    eigvectsback[2,2] = np.ones(t.shape)

    # Inicializa os autovetores do torus
    eigvectstorus = np.zeros(np.append((3,3),t.shape))
    eigvectstorus[2,0] = -np.ones(t.shape)

    # Modifica os autovetores pertencentes ao torus, tornando-os tangente 
    # à superficie do torus
    temp1 = (centro-y)/((centro-x)**2+(centro-y)**2)**0.5
    temp2 = (x-centro)/((centro-x)**2+(centro-y)**2)**0.5
    temp1[np.nonzero(np.isnan(temp1))] = 0
    temp2[np.nonzero(np.isnan(temp2))] = 0
    eigvectstorus[0,2] = temp1
    eigvectstorus[0,1] = temp2

    eigvectstorus[1,2] = temp2
    eigvectstorus[1,1] = -temp1

    # Calcula os autovetores para a imagem toda (combinando background+torus)
    eigvects = eigvectsback*(1-t)+eigvectstorus*t
    
    
    nd, sx, sy, sz = eigvals.shape
    
    #-----------------------------
    aux = eigvects[:,:,:,:,sx/2:] #aux = eigvects[:,0:2,:,:,sx/2:]
    
    eigvects[:,:,:,:,:sx/2] = aux #eigvects[:,0:2,:,:,:sx/2] = aux
    
    eigvects[:,:,:,:,sx/2:] = aux[:,:,:,::-1,::-1] #(Funciona melhor)

    return eigvals,eigvects




#Bifurcation
def sintV(l1, l2, l3, n, r, l_back1, l_back2, l_back3):
    import numpy as np
    
    a = (n-r)/(n/2) #inclinaçao da reta que vai do 0,0 até o "meio"
    b1 = 0

    z,y,x = np.mgrid[0:n,0:n,0:n]
    R = a*x + b1 - y #equacao da reta (voxels pertencentes a reta)
    R = np.where(((R**2) + (z-(n/2))**2)**0.5 < r) # distancia
    k,j,i = R
    vaux = np.zeros((n,n,n))
    vaux[k,j,i] = 1 #voxels pertencentes a metade do V

    v = np.zeros((n,n,n))
    v[:,:,:n/2] = vaux[:,:,:n/2]
    vaux2 = vaux[:,:,::-1]
    v[:,:,n/2:] = vaux2[:,:,n/2:] #voxels pertencentes ao V (1 onde pertence e 0 é background)


    # Inicializa os autovetores do background
    eigvectsback = np.zeros(np.append((3,3),x.shape))  # <----
    eigvectsback[0,0,:,:,:] = 1 #coloca os vetores ortogonais
    eigvectsback[1,1,:,:,:] = 1
    eigvectsback[2,2,:,:,:] = 1



    # autovetores do V
    # ev1
    ev1_1 = np.array([0,a,1])/(a**2 + 1)**0.5
    ev1_2 = np.array([0,a,-1])/(a**2 + 1)**0.5

    eigvectV = np.zeros(np.append((3,3),x.shape))
    eigvectV[0,2,:,:,:n/2] = ev1_1[2]*v[:,:,:n/2]
    eigvectV[0,2,:,:,n/2:] = ev1_2[2]*v[:,:,n/2:]
    eigvectV[0,1,:,:,:n/2] = ev1_1[1]*v[:,:,:n/2]
    eigvectV[0,1,:,:,n/2:] = ev1_2[1]*v[:,:,n/2:]
    #z do ev1 = 0 mesmo

    # ev2
    eigvectV[1,1,:,:,:] = eigvectV[0,2,:,:,:]
    eigvectV[1,2,:,:,:] = -eigvectV[0,1,:,:,:]

    # ev3
    eigvectV[2,0,:,:,:] = 1


    eigvect = eigvectV*v + (1-v)*eigvectsback

    #autovalores
    eigvalsV = [l1*np.ones((n,n,n)), l2*np.ones((n,n,n)), l2*np.ones((n,n,n))]

    eigvals_back = [l_back1*np.ones((n,n,n)), l_back2*np.ones((n,n,n)), l_back2*np.ones((n,n,n))]


    eigvals = eigvalsV*v + (1-v)*eigvals_back

    return eigvals,eigvect


# # Visualization

# In[1]:

def show_scalar_field(SM):
    
    # Show scalar map (FA, MD, etc..)
    
    import numpy as np
    # image and graphic
    from IPython.display import Image
    from IPython.display import display
    import matplotlib.pyplot as plt
    get_ipython().magic(u'matplotlib')
        
    # %matplotlib inline
#     %matplotlib notebook
    from matplotlib.widgets import Slider

    sz, sy, sx = SM.shape

    fig = plt.figure(figsize=(15,15))
    xy = fig.add_subplot(1,3,1)
    plt.title("Axial Slice")
    xz = fig.add_subplot(1,3,2)
    plt.title("Coronal Slice")
    yz = fig.add_subplot(1,3,3)
    plt.title("Sagittal Slice")

    # make the slider frame
    pos = 0
    axframe = plt.axes([0.25, 0.1+pos, 0.65, 0.03])
    sframe = Slider(axframe, 'Slice', 0, 1, valinit=0,valfmt='%f')

    s = 0

    #normalize for visualization purpose
    maximo = np.max(np.abs(SM)) # max e min usados para fazer o FA ocupar toda faixa 0-1
    minimo = np.min(np.abs(SM))

    xy.imshow(SM[s,:,:], origin='lower', interpolation='nearest', cmap="gray",vmin=0, vmax=maximo )
    xz.imshow(SM[:,s,:], origin='lower', interpolation='nearest', cmap="gray",vmin=0 , vmax=maximo )
    yz.imshow(SM[:,:,s], origin='lower', interpolation='nearest', cmap="gray",vmin=0 , vmax=maximo )


    plt.axis("off")

    def update(val):
        s = sframe.val
        xy.imshow(SM[int(np.floor(s*sz)),:,:], origin='lower', interpolation='nearest', cmap="gray",vmin=0 , vmax=maximo )
        xz.imshow(SM[:,int(np.floor(s*sy)),:], origin='lower', interpolation='nearest', cmap="gray",vmin=0 , vmax=maximo )
        yz.imshow(SM[:,:,int(np.floor(s*sx))], origin='lower', interpolation='nearest', cmap="gray",vmin=0 , vmax=maximo )
    #     plt.draw()

    # connect callback to slider   
    sframe.on_changed(update)
    plt.show()


# In[2]:

def show_vector_field_2(VF):
    
    # Show scalar map (FA, MD, etc..)
    
    
    import numpy as np
    # image and graphic
    from IPython.display import Image
    from IPython.display import display
    import matplotlib.pyplot as plt
    get_ipython().magic(u'matplotlib')
        
    # %matplotlib inline
#     %matplotlib notebook
    from matplotlib.widgets import Slider


    nv, sz, sy, sx = VF.shape

    fig = plt.figure(figsize=(15,15))
    xy = fig.add_subplot(1,3,1)
    plt.title("Axial Slice")
    plt.axis("off")
    xz = fig.add_subplot(1,3,2)
    plt.title("Coronal Slice")
    plt.axis("off")
    yz = fig.add_subplot(1,3,3)
    plt.title("Sagittal Slice")
    plt.axis("off")

    # make the slider frame
    pos = 0
    axframe = plt.axes([0.25, 0.1+pos, 0.65, 0.03])
    sframe = Slider(axframe, 'Slice', 0, 1, valinit=0,valfmt='%f')

    step_ = 1 #Subamostragem dos vetores
    maxlen_= 32 #Tamanho do maior vetor
    rescale_ = 16 #Fator de rescala da imagem

    s = 1
    # seismic
    V1 = show_vector_field(VF[1,s,:,:], VF[2,s,:,:], step=step_, maxlen=maxlen_, rescale=rescale_)
    xy.imshow(V1[0,:,:], origin='lower',cmap="gray")
    V2 = show_vector_field(VF[0,:,s,:], VF[2,:,s,:], step=step_, maxlen=maxlen_, rescale=rescale_)
    xz.imshow(V2[0,:,:], origin='lower',cmap="gray")
    V3 = show_vector_field(VF[0,:,:,s], VF[1,:,:,s], step=step_, maxlen=maxlen_, rescale=rescale_)
    yz.imshow(V3[0,:,:], origin='lower',cmap="gray")
    plt.xticks([])
    plt.yticks([])

    plt.axis("off")

    def update(val):
        s = sframe.val

        V1 = show_vector_field(VF[1,int(np.floor(s*sz)),:,:], VF[2,int(np.floor(s*sz)),:,:], step=step_, maxlen=maxlen_, rescale=rescale_)
        xy.imshow(V1[0,:,:], origin='lower',cmap="gray")
        V2 = show_vector_field(VF[0,:,int(np.floor(s*sy)),:], VF[2,:,int(np.floor(s*sy)),:], step=step_, maxlen=maxlen_, rescale=rescale_)
        xz.imshow(V2[0,:,:], origin='lower',cmap="gray")
        V3 = show_vector_field(VF[0,:,:,int(np.floor(s*sx))], VF[1,:,:,int(np.floor(s*sx))], step=step_, maxlen=maxlen_, rescale=rescale_)
        yz.imshow(V3[0,:,:], origin='lower',cmap="gray")

        plt.draw()

    # connect callback to slider   
    sframe.on_changed(update)
    plt.show()


# # Divergence and Curl

# In[2]:

# d = dFx/dx + dFy/dy + dFz/dz
# ([z y x] [Z] [Y] [X]), a entrada é um campo vetorial 3d
def divergence(v):
    dx = v[2,:,:,1:] - v[2,:,:,:-1]
    dx = (dx[:,1:,:] + dx[:,:-1,:])/2
    dx = (dx[1:,:,:] + dx[:-1,:,:])/2

    dy = v[1,:,1:,:] - v[1,:,:-1,:]
    dy = (dy[:,:,1:] + dy[:,:,:-1])/2
    dy = (dy[1:,:,:] + dy[:-1,:,:])/2

    dz = v[0,1:,:,:] - v[0,:-1,:,:]
    dz = (dz[:,1:,:] + dz[:,:-1,:])/2
    dz = (dz[:,:,1:] + dz[:,:,:-1])/2
    
    return dx+dy+dz

#----------------------------------------------------------------
# d = dFx/dx + dFy/dy + dFz/dz
# divergence look up table ([indice do campo vetorial] [z y x] [Z] [Y] [X]), a entrada é um campo vetorial 3d
def divergence_lut(evt_lut):
    dx = evt_lut[:,2,:,:,1:] - evt_lut[:,2,:,:,:-1]
    dx = (dx[:,:,1:,:] + dx[:,:,:-1,:])/2
    dx = (dx[:,1:,:,:] + dx[:,:-1,:,:])/2

    dy = evt_lut[:,1,:,1:,:] - evt_lut[:,1,:,:-1,:]
    dy = (dy[:,:,:,1:] + dy[:,:,:,:-1])/2
    dy = (dy[:,1:,:,:] + dy[:,:-1,:,:])/2

    dz = evt_lut[:,0,1:,:,:] - evt_lut[:,0,:-1,:,:]
    dz = (dz[:,:,1:,:] + dz[:,:,:-1,:])/2
    dz = (dz[:,:,:,1:] + dz[:,:,:,:-1])/2

    return dx+dy+dz
#----------------------------------------------------------------
# r = [dFy/dx - dFx/dy] [dFx/dz - dFz/dx] [dFz/dy - dFy/dz]
# ([z y x] [Z] [Y] [X]), a entrada é um campo vetorial 3d
# ([z y x] [Z] [Y] [X]), a saída é um campo vetorial 3d
def rotacional(v):
    dzy = v[0,:,1:,:] - v[0,:,:-1,:] #dFz/dy
    dzy = (dzy[:,:,1:] + dzy[:,:,:-1])/2
    dzy = (dzy[1:,:,:] + dzy[:-1,:,:])/2

    dyz = v[1,1:,:,:] - v[1,:-1,:,:] #dFy/dz
    dyz = (dyz[:,1:,:] + dyz[:,:-1,:])/2
    dyz = (dyz[:,:,1:] + dyz[:,:,:-1])/2
    #---------------------------------------
    dxz = v[2,1:,:,:] - v[2,:-1,:,:] #dFx/dz
    dxz = (dxz[:,1:,:] + dxz[:,:-1,:])/2
    dxz = (dxz[:,:,1:] + dxz[:,:,:-1])/2

    dzx = v[0,:,:,1:] - v[0,:,:,:-1] #dFz/dx
    dzx = (dzx[:,1:,:] + dzx[:,:-1,:])/2
    dzx = (dzx[1:,:,:] + dzx[:-1,:,:])/2
    #---------------------------------------
    dyx = v[1,:,:,1:] - v[1,:,:,:-1] #dFy/dx
    dyx = (dyx[:,1:,:] + dyx[:,:-1,:])/2
    dyx = (dyx[1:,:,:] + dyx[:-1,:,:])/2

    dxy = v[2,:,1:,:] - v[2,:,:-1,:] #dFx/dy
    dxy = (dxy[:,:,1:] + dxy[:,:,:-1])/2
    dxy = (dxy[1:,:,:] + dxy[:-1,:,:])/2
    #---------------------------------------

    r = np.squeeze(np.array([[dyx - dxy], [dxz - dzx], [dzy - dyz]]), axis=(1,))

    return r


# # Plane fitting

# In[7]:

# calcula o melhor plano para cada um das direçoes de interesse (numero de iteraçoes)
def fitting_planes_2(div_tre_abs, Directions, n_min_points=5, n_max_interations=8, max_dist=2, percentile=10):

    import numpy as np
    
    
    na, sz, sy, sx = div_tre_abs.shape


    n_angles,_,_,_ = div_tre_abs.shape
    mean_error = np.ones((n_angles))*1000
    prod_int = np.ones((n_angles))*2
    NORMAL = np.zeros((n_angles,3))
    D_p = np.zeros(n_angles)
    N_iterations = np.zeros(n_angles)

    # for i in range(2, 23):
    for i in range(0, n_angles):
        data = np.where(div_tre_abs[i] > 0)
        data = np.asarray(data)
        data = data.T

        n_points,_ = data.shape
        
        max_dist_calc = 50
        count = 0

        if n_points > n_min_points:
            while ((count < n_max_interations) and (max_dist < max_dist_calc) and (n_points > n_min_points)):
                # calcula o plano
                normal_ls, d_ls = planefromcloud(sz, sy, data)

                #distance from points to plane
                dist_PP = dist_points_plane(normal_ls, d_ls, data)

                percentile_calc = np.percentile(dist_PP,100-percentile)
                if percentile_calc > max_dist:
                    keep = np.where(dist_PP < percentile_calc)
                else:
                    keep = np.where(dist_PP <= max_dist)

                data = data[keep]
                n_points,_ = data.shape

                max_dist_calc = np.max(dist_PP[keep])
                count = count + 1

            NORMAL[i] = normal_ls/np.linalg.norm(normal_ls)
            D_p[i] = d_ls

    #         prod_int[i] = np.absolute(np.dot(Directions[i], NORMAL[i]))
            prod_int[i] = np.dot(Directions[i], NORMAL[i])
            mean_error[i] = np.sum(dist_PP[keep])/n_points
            
            N_iterations[i] = count
            
    return NORMAL, D_p, prod_int, mean_error, N_iterations


def planefromcloud(sx = 20, sy = 90, data = 0): #o calculo é na orden XYZ, mas estou trocando X com Z para nao dar vetor com componente z infinito
    import scipy.linalg # pip install scipy
    import numpy as np  # pip install numpy
    
    #least square
    # regular grid covering the domain of the data
    X,Y = np.meshgrid(np.arange(0, sx, 5), np.arange(0, sy, 5))
    XX = X.flatten()
    YY = Y.flatten()

    # best-fit linear plane
    A = np.c_[data[:,0], data[:,1], np.ones(data.shape[0])]
    C,res,_,_ = scipy.linalg.lstsq(A, data[:,2])    # coefficients
    # evaluate it on grid
    Z = C[0]*X + C[1]*Y + C[2]


    normal_ls = [-C[0],-C[1],1]

    z_aux = C[0] + C[1] + C[2]
    d_ls = -normal_ls[0] - normal_ls[0] - z_aux
    
    return normal_ls, d_ls #a b c d

def dist_points_plane(normal_ls, d_ls, data):
    import numpy as np
    
    #distance from points to plane
    dist_PP = np.absolute(normal_ls[0]*data[:,0] + normal_ls[1]*data[:,1] + normal_ls[2]*data[:,2] + d_ls)/np.linalg.norm(normal_ls)
    
    return dist_PP

# calcula a melhor reta removendo outliars (parece que não está tao robusto)
def fitting_reta(y, x, n_min_points=40, n_max_interations=40, max_dist=0.4, percentile=2):

    import numpy as np
    
    n_points = y.shape
        
    count = 0
    max_dist_calc = 1
    
    if n_points > n_min_points:
        while ((count < n_max_interations) and (max_dist < max_dist_calc) and (n_points > n_min_points)):
            # calcula o plano
            fit = np.polyfit(x,y,1)

            #distance from points to line
            ax = x*fit[0]
            by = -y
            c = np.ones(y.shape)*fit[1]
            dist = np.abs(ax + by + c)/np.linalg.norm(fit)

            percentile_calc = np.percentile(dist,100-percentile)
            if percentile_calc > max_dist:
                keep = np.where(dist < percentile_calc)
            else:
                keep = np.where(dist <= max_dist)

            x = x[keep]
            y = y[keep]
            n_points = y.shape

            max_dist_calc = np.max(dist[keep])
            count = count + 1
        
        root = -fit[1]/fit[0]
#         print('root = ', root)
            
    return y, x, root, fit


#Retorna angulos dado o vetor nolmal ao plano
# alpha = angulo entre o plano axial e o vetor
# theta = angulo entre o plano sagital e o vetor
def angle_from_vector_2(vector): #vactor = [z x y]
    import numpy as np
    
    vector = vector/(np.linalg.norm(vector))
    
    alpha = np.arcsin(vector[0])*180/np.pi
    theta = np.arcsin(vector[1])*180/np.pi
    
    return alpha, theta


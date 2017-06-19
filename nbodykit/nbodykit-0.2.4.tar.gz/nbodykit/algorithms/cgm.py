import numpy
import logging

import kdcount
import pandas as pd
from nbodykit import CurrentMPIComm
from nbodykit.source.catalog import ArrayCatalog


class CylindricalGroups(object):
    """
    Compute groups of objects using a cylindrical grouping method. We identify
    all satellites within a given cylindrical volume around a central object

    Reference
    ---------
    Okumura, Teppei, et al. "Reconstruction of halo power spectrum from
    redshift-space galaxy distribution: cylinder-grouping method and halo
    exclusion effect", arXiv:1611.04165, 2016.
    """
    logger = logging.getLogger('CylindricalGroups')

    def __init__(self, source, rperp, rpar, periodic=True, los=[0,0,1], BoxSize=None):
        """
        Parameters
        ----------
        source : CatalogSource
            the input source of particles providing the 'Position' column; the
            grouping algorithm is run on this catalog
        rperp : float
            the radius of the cylinder in the sky plane (i.e., perpendicular
            to the line-of-sight)
        rpar : float
            the radius along the line-of-sight direction; this is 1/2 the
            height of the cylinder
        periodic : bool; optional
            whether to use periodic boundary conditions
        """
        if 'Position' not in source:
            raise ValueError("the 'Position' column must be defined in the source")

        self.source = source
        self.comm = source.comm
        self.attrs = {}

        # need BoxSize
        self.attrs['BoxSize'] = numpy.empty(3)
        BoxSize = source.attrs.get('BoxSize', BoxSize)
        if periodic and BoxSize is None:
            raise ValueError("please specify a BoxSize if using periodic boundary conditions")
        self.attrs['BoxSize'][:] = BoxSize

        # save meta-data
        self.attrs['rpar'] = rpar
        self.attrs['rperp'] = rperp
        self.attrs['periodic'] = periodic

        self.run()

    def run(self):
        """
        Compute the three-point CF multipoles. This attaches the following
        the attributes to the class:

        Attributes
        ----------
        poles : :class:`~nbodykit.dataset.DataSet` or ``None``
            a DataSet object to hold the multipole results
        """
        from pmesh.domain import GridND
        import mpsort

        comm = self.comm
        if self.attrs['periodic']:
            boxsize = self.attrs['BoxSize']
        else:
            boxsize = None

        # determine processor division for domain decomposition
        for Nx in range(int(comm.size**0.3333) + 1, 0, -1):
            if comm.size % Nx == 0: break
        else:
            Nx = 1
        for Ny in range(int(comm.size**0.5) + 1, 0, -1):
            if (comm.size // Nx) % Ny == 0: break
        else:
            Ny = 1
        Nz = comm.size // Nx // Ny
        Nproc = [Nx, Ny, Nz]
        if self.comm.rank == 0:
            self.logger.info("using cpu grid decomposition: %s" %str(Nproc))

        # get the position
        cols = self.source['Position'], self.source['halo_mvir'], self.source['gal_type']
        pos1, mass, gal_type = self.source.compute(*cols)

        # global min/max across all ranks
        posmin = numpy.asarray(comm.allgather(pos1.min(axis=0))).min(axis=0)
        posmax = numpy.asarray(comm.allgather(pos1.max(axis=0))).max(axis=0)

        # domain decomposition
        grid = [numpy.linspace(posmin[i], posmax[i], Nproc[i]+1, endpoint=True) for i in range(3)]
        domain = GridND(grid, comm=comm)

        # exhange across ranks
        layout = domain.decompose(pos1, smoothing=0)
        pos1 = layout.exchange(pos1)
        mass = layout.exchange(mass)
        gal_type = layout.exchange(gal_type)

        # sort
        dtype = numpy.dtype([
                ('origind', 'u4'),
                ('mass', mass.dtype),
                ('gal_type', gal_type.dtype),
                ('pos', (pos1.dtype.str, 3))
                ])
        data = numpy.empty(len(self.source), dtype=dtype)
        data['mass'] = mass
        data['gal_type'] = gal_type
        data['pos'] = pos1
        data['origind'] = numpy.arange(len(data), dtype='u4')
        data['origind'] += sum(self.comm.allgather(len(data))[:self.comm.rank])

        # sort pos1 by mass and then gal type
        data.sort(order=['mass', 'gal_type'])
        pos1 = data['pos']

        # the maximum distance still inside the cylinder
        rperp, rpar = self.attrs['rperp'], self.attrs['rpar']
        rmax = (rperp**2 + rpar**2)**0.5

        # exchange the positions
        layout  = domain.decompose(pos1, smoothing=rmax)
        pos2 = layout.exchange(pos1)

        # make the KD-tree
        tree1 = kdcount.KDTree(pos1, boxsize=boxsize).root
        tree2 = kdcount.KDTree(pos2, boxsize=boxsize).root
        los = numpy.array([0, 0, 1])

        rperp2 = self.attrs['rperp']**2

        out = []
        def callback(r, i, j):

            r1 = pos1[i]
            r2 = pos2[j]
            dr = r1 - r2

            # enforce periodicity in dpos
            if self.attrs['periodic']:
                for axis, col in enumerate(dr.T):
                    col[col > boxsize[axis]*0.5] -= boxsize[axis]
                    col[col <= -boxsize[axis]*0.5] += boxsize[axis]

            # los distance
            rlos =  numpy.einsum("ij,j->i", dr, los)

            # sky
            dr2 = numpy.einsum('ij, ij->i', dr, dr)
            rsky2 = numpy.abs(dr2 - rlos ** 2)
            valid = (i<j)&(rsky2 <= rperp2)&(abs(rlos) <= self.attrs['rpar'])

            data = numpy.vstack([i[valid], j[valid]]).T
            out.append(data)

        # enum the tree
        tree1.enum(tree2, rmax, process=callback)

        # and save
        out = numpy.concatenate(out, axis=0)
        df = pd.DataFrame(out, columns=['i', 'j'])
        self.df = df

        # initialize output
        N_cgm = numpy.zeros(len(self.source), dtype='i8')
        cgm_gal_type = numpy.zeros(len(self.source), dtype='i4') - 1
        cen_id = numpy.zeros(len(self.source), dtype='i8') - 1

        # group by centrals
        cens_grouped = df.groupby('i')

        # loop over all CGM groups
        for cen_num, group in cens_grouped:

            orig_cenid = data['origind'][cen_num]
            sat_indices = group['j'].values
            orig_sat_indices = data['origind'][sat_indices]

            # new objects must be unmarked
            if cgm_gal_type[orig_cenid] == -1:

                # this must be a central
                cgm_gal_type[orig_cenid] = 0

                # only unidentified satellites can be added to this central
                isnew = cgm_gal_type[orig_sat_indices] == -1
                cgm_gal_type[orig_sat_indices[isnew]] = 1
                cen_id[orig_sat_indices[isnew]] = orig_cenid

                # store the number of sats in this halo
                N_cgm[orig_cenid] = isnew.sum()

        # any unmarked objects are centrals with no satellite matches
        cgm_gal_type[cgm_gal_type==-1] = 0

        # make the structured data
        dtype = numpy.dtype([('num_cgm_sats', 'i8'), ('cgm_gal_type', 'i4'), ('cgm_cenid', 'i8')])
        data = numpy.empty(len(self.source), dtype=dtype)

        data['num_cgm_sats'] = N_cgm
        data['cgm_gal_type'] = cgm_gal_type
        data['cgm_cenid'] = cen_id

        self.groups = ArrayCatalog(data, comm=self.comm, **self.attrs)


    # def __getstate__(self):
    #     return {'poles':self.poles.data, 'attrs':self.attrs}
    #
    # def __setstate__(self, state):
    #     self.__dict__.update(state)
    #     self.poles = DataSet(['r1', 'r2'], [self.attrs['edges']]*2, self.poles)
    #
    # def save(self, output):
    #     """
    #     Save result as a JSON file
    #     """
    #     import json
    #     from nbodykit.utils import JSONEncoder
    #
    #     # only the master rank writes
    #     if self.comm.rank == 0:
    #         self.logger.info('measurement done; saving result to %s' % output)
    #
    #         with open(output, 'w') as ff:
    #             json.dump(self.__getstate__(), ff, cls=JSONEncoder)
    #
    # @classmethod
    # @CurrentMPIComm.enable
    # def load(cls, output, comm=None):
    #     """
    #     Load a result has been saved to disk with :func:`save`.
    #     """
    #     import json
    #     from nbodykit.utils import JSONDecoder
    #     if comm.rank == 0:
    #         with open(output, 'r') as ff:
    #             state = json.load(ff, cls=JSONDecoder)
    #     else:
    #         state = None
    #     state = comm.bcast(state)
    #     self = object.__new__(cls)
    #     self.__setstate__(state)
    #     self.comm = comm
    #     return self

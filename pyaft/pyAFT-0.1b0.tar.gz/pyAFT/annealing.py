import pylab as plt
from scipy.interpolate import interp1d


class annealModel():

    def __init__(self, c0, c1, c2, c3, a, b, lmin):
        self.c0 = c0
        self.c1 = c1
        self.c2 = c2
        self.c3 = c3
        self.a = a
        self.b = b
        self.lmin = lmin


class CalibCurve():
    """Calibration Curve class.

    Useful to work with experimentaly established curved
    """
    
    def __init__(self, pts, xlabel, ylabel, source=""):
        self.pts = pts
        self.x = [x for x, y in pts]
        self.y = [y for x, y in pts]
        self.xlabel = xlabel
        self.ylabel = ylabel
        self.source = source

    def getval(self, x, kind="linear"):
        """Get interpolated value at x.
        
        Parameters:
        ----------
        x -- position (array of position)
        kind -- interpolation kind ("linear"(default), "cubic")

        Returns:
        -------
        array
        """

        f = interp1d(self.x, self.y, kind=kind)
        return f(x)

    def show(self):
        """Plot Calibration curve"""
        plt.figure()
        plt.plot(self.x, self.y)
        plt.xlabel(self.xlabel)
        plt.ylabel(self.ylabel)
        plt.title(self.source)
        plt.show()


# List of Annealing models
KetchamEtAl = annealModel(c0=-19.844,
                          c1=0.38951,
                          c2=-51.253,
                          c3=-7.6423,
                          a=-0.12327,
                          b=-11.988,
                          lmin=0.0)

TILm = annealModel(c0=-1.66965,
                   c1=0.0000241755,
                   c2=-12.4864,
                   c3=0.000843004,
                   a=0.675508,
                   b=4.16615,
                   lmin=0.0)

TILc = annealModel(c0=-2.36910,
                   c1=0.0000603834,
                   c2=-8.65794,
                   c3=0.000972676,
                   a=0.404700,
                   b=1.65355,
                   lmin=9.0)

CrowDur = annealModel(c0=-3.202,
                      c1=0.00009367,
                      c2=-19.6328,
                      c3=0.0004200,
                      a=0.49,
                      b=3.00,
                      lmin=0.0)

CrowFAp = annealModel(c0=-1.508,
                      c1=0.00002076,
                      c2=-10.3227,
                      c3=0.0009967,
                      a=0.76,
                      b=4.30,
                      lmin=0.0)

CrowSrAp = annealModel(c0=-1.123,
                       c1=0.00001055,
                       c2=-5.0085,
                       c3=0.001195,
                       a=0.97,
                       b=4.16,
                       lmin=0.0)

LasDur = annealModel(c0=-4.87,
                     c1=0.000168,
                     c2=-28.12,
                     c3=0.0,
                     a=0.35,
                     b=2.7,
                     lmin=0.0)


# This is the curve describing the relationship between
# Reduced Mean Length and C projected length
# Useful to calculate projected lengths
reduced_MeanLength_vs_Reduced_Cparallel = CalibCurve(pts=[(1.0, 1.0),
                                                     (0.95881, 0.970588),
                                                     (0.917508, 0.941176),
                                                     (0.876082, 0.911765),
                                                     (0.834515, 0.882353),
                                                     (0.792789, 0.852941),
                                                     (0.750883, 0.823529),
                                                     (0.708769, 0.794118),
                                                     (0.666416, 0.764706),
                                                     (0.644024, 0.735294),
                                                     (0.592261, 0.705882),
                                                     (0.543816, 0.676471),
                                                     (0.499281, 0.647059),
                                                     (0.460204, 0.617647),
                                                     (0.428183, 0.588235),
                                                     (0.403557, 0.558824),
                                                     (0.385398, 0.529412),
                                                     (0.0, 0.0)],
                                                     xlabel="Reduced Mean Length",
                                                     ylabel="C parallel length")

lengthToDensity = CalibCurve(pts=[(1.0, 1.0),
                             (0.95881, 0.956529),
                             (0.917508, 0.912921),
                             (0.876082, 0.869161),
                             (0.834515, 0.82523),
                             (0.792789, 0.781104),
                             (0.750883, 0.736758),
                             (0.708769, 0.692159),
                             (0.666416, 0.647269),
                             (0.644024, 0.541049),
                             (0.592261, 0.442989),
                             (0.543816, 0.358767),
                             (0.499281, 0.286844),
                             (0.460204, 0.225362),
                             (0.428183, 0.172461),
                             (0.403557, 0.126281),
                             (0.385398, 0.085095),
                             (0.0, 0.0)],
                             xlabel="Length",
                             ylabel="Density")


import unittest
# import unittest2 as unittest # for versions of python < 2.7

"""
        Method                  Checks that
self.assertEqual(a, b)           a == b   
self.assertNotEqual(a, b)        a != b   
self.assertTrue(x)               bool(x) is True  
self.assertFalse(x)              bool(x) is False     
self.assertIs(a, b)              a is b
self.assertIsNot(a, b)           a is not b
self.assertIsNone(x)             x is None 
self.assertIsNotNone(x)          x is not None 
self.assertIn(a, b)              a in b
self.assertNotIn(a, b)           a not in b
self.assertIsInstance(a, b)      isinstance(a, b)  
self.assertNotIsInstance(a, b)   not isinstance(a, b)  

See:
      https://docs.python.org/2/library/unittest.html
         or
      https://docs.python.org/dev/library/unittest.html
for more assert options
"""

import sys, os

here = os.path.abspath(os.path.dirname(__file__)) # Needed for py.test
up_one = os.path.split( here )[0]  # Needed to find digiplot development version
if here not in sys.path[:2]:
    sys.path.insert(0, here)
if up_one not in sys.path[:2]:
    sys.path.insert(0, up_one)

from digiplot.plot_image import PlotImage

class MyTest(unittest.TestCase):

    def setUp(self):
        unittest.TestCase.setUp(self)
        self.myclass = PlotImage(1000, 1000)

    def tearDown(self):
        unittest.TestCase.tearDown(self)
        del( self.myclass )

    def test_should_always_pass_cleanly(self):
        """Should always pass cleanly."""
        pass

    def test_myclass_existence(self):
        C = self.myclass
        self.assertTrue(C)
        self.assertEqual(C.i_origin, 100)
        self.assertEqual(C.j_origin, 900)

    def test_set_origin_xy(self):
        C = self.myclass
        C.set_origin_xy( 10., 1000. )
        self.assertEqual( (C.x_origin,C.y_origin), (10., 1000.))

    def test_set_ix_origin(self):
        C = self.myclass
        C.set_ix_origin(10, 99.9)
        self.assertEqual( (C.i_origin,C.x_origin), (10, 99.9))

    def test_set_jy_origin(self):
        C = self.myclass
        C.set_jy_origin(10, 99.9)
        self.assertEqual( (C.j_origin,C.y_origin), (10, 99.9))

    def test_define_origin_ij(self):
        C = self.myclass
        C.define_origin_ij(500, 500)
        self.assertEqual( (C.i_origin,C.j_origin), (500, 500))

    def test_set_imax_xmax(self):
        C = self.myclass
        C.set_imax_xmax(222, 222.)
        self.assertEqual( (C.imax,C.xmax), (222, 222.0))

    def test_set_jmax_ymax(self):
        C = self.myclass
        C.set_jmax_ymax(222, 222.)
        self.assertEqual( (C.jmax,C.ymax), (222, 222.0))

    def test_get_xy_at_ij(self):
        x,y = self.myclass.get_xy_at_ij(900, 100)
        
        self.assertEqual((x,y), (1.,1.))

    def test_get_a_few_xy_at_ij(self):
        x,y = self.myclass.get_xy_at_ij(800, 200)
        self.assertEqual((x,y), (0.875, 0.875))

        x,y = self.myclass.get_xy_at_ij(500, 500)
        self.assertEqual((x,y), (0.5, 0.5))


if __name__ == '__main__':
    # Can test just this file from command prompt
    #  or it can be part of test discovery from nose, unittest, pytest, etc.
    unittest.main()


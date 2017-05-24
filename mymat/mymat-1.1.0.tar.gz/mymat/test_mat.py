import unittest

import mymat

class TestMyMat(unittest.TestCase):

    def almostEqual(self, *As, **kw):
        for k, A in enumerate(As):
            for B in As[k+1:]:
                if not self.assertAlmostEqual((A-B).norm(), 0, **kw):
                    return False
        return True

    def test_mymat(self):
        A=mymat.H(4)
        self.assertIsInstance(A[1,2:4], mymat.MyMat)

    def test_size(self):
        A=mymat.H(7)
        self.assertEqual(A[[1,3,5],:].shape, (3, 7))
        B=A.delete(slice(1,4), [1,7])
        A[1:4,[1,7]]=[]
        self.assertEqual(A.shape, (3, 5))
        self.assertEqual(B.shape, (3, 5))
        C=B.delete([],4)
        self.assertEqual(C.shape, (3, 4))
        D = B.copy()
        D[[],4]=[]
        self.assertEqual(D.shape, (3, 4))

    def test_get(self):
        A=mymat.MyMat.random(7)
        B=A[[1,2,4],[5, 7]]
        C=A[[-6, -5, -3], [-2, 0]]
        D=A(([-6, -5, -3], [-2, 0]))
        self.assertTrue(mymat.equal(B, C, D))

        A=mymat.TestMat(7)
        B=A[[1, 2, 4],[5, 7]].tovec(2)
        C=A[[29, 43, 30, 44, 32, 46]]
        D=A([29, 43, 30, 44, 32, 46])
        self.assertTrue(mymat.equal(B, C, D))


    def test_op(self):
        A=mymat.H(3)
        self.almostEqual((1/A)*A, mymat.I(3), A/A, A*A.I)
        A=mymat.MyMat.ones(4)
        self.assertTrue(mymat.equal(A^3, A*A*A))
        A=mymat.H(3)
        self.assertTrue(mymat.equal(A//A, mymat.MyMat.ones(3)))

    def test_set(self):
        # sigle index
        A=mymat.TestMat(4)
        C=A.copy()
        A[[1,4,5,8]]=5  # =[[5,5],[5,5]]
        C[[1,4],[1,2]]=[5,5,5,5]
        self.assertTrue(mymat.equal(A, C))
        A[[1,17]]=5
        C[1,[1,5]]=[5,5]
        self.assertTrue(mymat.equal(A, C))

        # double index
        T = mymat.TestMat(5,3)
        T2 = mymat.TestMat(3)
        A = T2
        A[[4,5],[1,2,3]]=[10,11,12,13,14,15]
        self.assertTrue(A.equal(T))
        A = T2
        A[4:5,[1,2,3]] = [[10,11,12],[13,14,15]]
        self.assertTrue(A.equal(T))
        A = T2
        A[4:5,1:3] = mymat.BaseMatrix([[10,11,12], [13,14,15]])
        self.assertTrue(A.equal(T))
        A[5:4:-1,1:3] = [[13,14,15], [10,11,12]]
        self.assertTrue(A.equal(T))

    def test_just(self):
        A=mymat.TestMat(3)
        A.just(2,-6)
        self.assertEqual(A.shape, (2, 6))

    # def test_withpy(self):
    #     from mymat import pymat
    #     A=mymat.H(5)
    #     B=pymat.H(5)
    #     self.assertTrue(equal(A,B))
    #     self.assertTrue(equal(A[1:2,1:2],B[0:2,0:2]))
    #     A[1:2,1:2]=[[9,9],[8,8]]
    #     B[0:2,0:2]=[[9,9],[8,8]]
    #     self.assertTrue(equal(A,B))



if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TestMyMat)
    unittest.TextTestRunner(verbosity=2).run(suite)

from __future__ import print_function

import unittest

from contextional import GroupContextManager as GCM


class T(object):

    def assertThing(self, arg):
        assert arg == 4


GCM.utilize_asserts(T)



#
# with GCM("TEst") as t:
#
#     @t.add_test("stuff")
#     def test(case):
#         case.assertThing(4)
#
#     with t.add_group("other"):
#         @t.add_test("stuff")
#         def test(case):
#             case.assertThing(2)
#
#
# with GCM("Predefined Group") as PG:
#
#     @PG.add_test("value is 1")
#     def test(case):
#         case.assertEqual(
#             PG.value,
#             1,
#         )
#
#     with PG.add_group("Sub Group"):
#
#         @PG.add_test("value is still 1")
#         def test(case):
#             case.assertEqual(
#                 PG.value,
#                 1,
#             )

def multiplier(num_1, num_2):
    return num_1 * num_2


with GCM("value test") as vt:

    @vt.add_test("value")
    def test(case):
        case.assertEqual(
            vt.value,
            vt.expected_value,
        )

x = list("abcde")

with GCM("Main Group") as MG:

    @MG.add_teardown
    def tearDown():
        pass

    for l in x:

        with MG.add_group(l):

            @MG.add_setup
            def setUp(l=l):
                MG.l = l

            @MG.add_test("letter: {}".format(l))
            def test(case):

                case.assertIn(
                    MG.l,
                    "abcd",
                )

            @MG.add_teardown
            def tearDown():
                pass

MG.create_tests(globals())

with GCM("Main Group") as MG2:

    @MG2.add_teardown
    def tearDown():
        pass

    for l in x:

        with MG2.add_group(l):

            @MG2.add_setup
            def setUp(l=l):
                MG2.l = l

            @MG2.add_test("letter: {}".format(l))
            def test(case):

                case.assertIn(
                    MG2.l,
                    "bcde",
                )

            @MG2.add_teardown
            def tearDown():
                pass

MG2.create_tests(globals())

def test():
    pass


if __name__ == '__main__':
    unittest.main()

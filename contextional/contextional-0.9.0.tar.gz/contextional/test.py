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

    @MG.add_test("will not pass")
    def test(case):
        case.fail(xy)

    with MG.add_group("Sub Group"):

        @MG.add_setup
        def setUp():
            raise Exception()

        @MG.add_test("will not pass")
        def test(case):
            case.fail()


MG.create_tests(globals())

# def test():
#     pass


if __name__ == '__main__':
    unittest.main()

'''    from __experimental__ import int_seq

makes it possible to use an alternative syntax instead of using `range`
in a for loop.  To be more specific, instead of

    for i in range(3):
        print(i)

we could write

    for i in 0 <= i < 3:
        print(i)

or

    for i in 0 <= i <= 2:   # compare upper boundary with previous case
        print(i)

By reversing the order of the comparison operators, we iterate in reverse.
Thus, for example

    for i in 10 >= i > 0:
        print(i)

would be equivalent to

    for i in range(10, 0, -1):
        print(i)

An additional condition can be added; for example

    for i in 1 <= i < 10  if (i % 2 == 0):
        print(i)

would print the first 4 even integers.

In addition, `inseq` is possible to use as a keyword instead of `in`.
`inseq` is meant to mean `in sequence`. Also, the "range" can be enclosed
in parentheses for greater clarity. Thus, the following is valid:

    for i inseq (1 <= i < 10)  if (i % 2 == 0):
        print(i)

The transformation is done using a regex search and is only valid
on a single line. **There is no guarantee that all legitimately
valid cases will be recognized as such.**
'''
import builtins
import re

def __experimental_range(start, stop, var, cond, loc={}):
    '''Utility function made to reproduce range() with unit integer step
       but with the added possibility of specifying a condition
       on the looping variable  (e.g. var % 2  == 0)
    '''
    locals().update(loc)
    if start < stop:
        for __ in range(start, stop):
            locals()[var] = __
            if eval(cond, globals(), locals()):
                yield __
    else:
        for __ in range(start, stop, -1):
            locals()[var] = __
            if eval(cond, globals(), locals()):
                yield __

builtins.__experimental_range = __experimental_range

######################################################################
#
#  WARNING
#
#  In the unlikely case that you know less about regular expressions than I do
#  please do not use what I do as any indication of how one should use regular
#  expressions (regex).
#
#  The regex use below is admitedly awful, very likely sub-optimal,
#  and could almost certainly be vastly improved upon, either by someone
#  who actually knows how to use regular expressions effectively or,
#  even better, by not using regular expressions at all, and either using
#  Python's tokenize module, or writing a custom parser.
#
#######################################################################

no_condition = r"""(?P<indented_for>\s*for\s+)
                      (?P<var>[a-zA-Z_]\w*)
                      \s+ (in|inseq) \s*
                      \(?\s*     # optional opening (
                      (?P<start>[-\w]+)
                      \s* %s \s*
                      (?P=var)
                      \s* %s \s*
                      (?P<stop>[-\w]+)
                      \s*\)?     # optional closing )
                      \s* : \s*
                      """
# A problem with the optional () is that the regex will be
# satisfied if only one of them is present. We'll take care of
# this by ensuring an equal number of opening and closing parentheses.

cases = []
le_lt = re.compile(no_condition % ("<=", "<"), re.VERBOSE)
cases.append((le_lt, "{0} {1} in range({2}, {3}):"))

le_le = re.compile(no_condition % ("<=", "<="), re.VERBOSE)
cases.append((le_le, "{0} {1} in range({2}, {3}+1):"))

lt_lt = re.compile(no_condition % ("<", "<"), re.VERBOSE)
cases.append((lt_lt, "{0} {1} in range({2}+1, {3}):"))

lt_le = re.compile(no_condition % ("<", "<="), re.VERBOSE)
cases.append((lt_le, "{0} {1} in range({2}+1, {3}+1):"))

ge_gt = re.compile(no_condition % (">=", ">"), re.VERBOSE)
cases.append((ge_gt, "{0} {1} in range({2}, {3}, -1):"))

ge_ge = re.compile(no_condition % (">=", ">="), re.VERBOSE)
cases.append((ge_ge, "{0} {1} in range({2}, {3}-1, -1):"))

gt_gt = re.compile(no_condition % (">", ">"), re.VERBOSE)
cases.append((gt_gt, "{0} {1} in range({2}-1, {3}, -1):"))

gt_ge = re.compile(no_condition % (">", ">="), re.VERBOSE)
cases.append((gt_ge, "{0} {1} in range({2}-1, {3}-1, -1):"))

with_condition = r"""(?P<indented_for>\s*for\s+)
                      (?P<var>[a-zA-Z_]\w*)
                      \s+ (in|inseq) \s*
                      \(?\s*     # optional opening (
                      (?P<start>[-\w]+)
                      \s* %s \s*
                      (?P=var)
                      \s* %s \s*
                      (?P<stop>[-\w]+)
                      \s*\)?     # optional closing )
                      \s* if \s+
                      (?P<cond>.+)
                      \s* : \s*
                      """
le_lt_cond = re.compile(with_condition % ("<=", "<"), re.VERBOSE)
cases.append((le_lt_cond, "{0} {1} in __experimental_range({2}, {3}, '{1}', '{4}', loc=locals()):"))

le_le_cond = re.compile(with_condition % ("<=", "<="), re.VERBOSE)
cases.append((le_le_cond, "{0} {1} in __experimental_range({2}, {3}+1, '{1}', '{4}', loc=locals()):"))

lt_lt_cond = re.compile(with_condition % ("<", "<"), re.VERBOSE)
cases.append((lt_lt_cond, "{0} {1} in __experimental_range({2}+1, {3}, '{1}', '{4}', loc=locals()):"))

lt_le_cond = re.compile(with_condition % ("<", "<="), re.VERBOSE)
cases.append((lt_le_cond, "{0} {1} in __experimental_range({2}+1, {3}+1, '{1}', '{4}', loc=locals()):"))

ge_gt_cond = re.compile(with_condition % (">=", ">"), re.VERBOSE)
cases.append((ge_gt_cond, "{0} {1} in __experimental_range({2}, {3}, '{1}', '{4}', loc=locals()):"))

ge_ge_cond = re.compile(with_condition % (">=", ">="), re.VERBOSE)
cases.append((ge_ge_cond, "{0} {1} in __experimental_range({2}, {3}-1, '{1}', '{4}', loc=locals()):"))

gt_gt_cond = re.compile(with_condition % (">", ">"), re.VERBOSE)
cases.append((gt_gt_cond, "{0} {1} in __experimental_range({2}-1, {3}, '{1}', '{4}', loc=locals()):"))

gt_ge_cond = re.compile(with_condition % (">", ">="), re.VERBOSE)
cases.append((gt_ge_cond, "{0} {1} in __experimental_range({2}-1, {3}-1, '{1}', '{4}', loc=locals()):"))


def transform_source(source):
    lines = source.split("\n")
    new_lines = []
    for line in lines:
        begin = line.split("#")[0]
        for (pattern, for_str) in cases:
            result = pattern.search(begin)
            if result is not None and begin.count('(') == begin.count(')'):
                line = create_for(for_str, result)
                break
        new_lines.append(line)
    return "\n".join(new_lines)


def create_for(line, search_result):
    '''Create a new "for loop" line as a replacement for the original code.
    '''
    try:
        return line.format(search_result.group("indented_for"),
                           search_result.group("var"),
                           search_result.group("start"),
                           search_result.group("stop"),
                           search_result.group("cond"))
    except IndexError:
        return line.format(search_result.group("indented_for"),
                           search_result.group("var"),
                           search_result.group("start"),
                           search_result.group("stop"))

from hypothesis import strategies as st
from hypothesis import given

from ..ppgr import Point, Points


def to_points(ps):
    return list([Point(p[0], p[1]) for p in ps])


@given(
    limit=st.integers(min_value=1),
    ps=st.lists(st.tuples(st.floats(), st.floats())))
def test_points_limit(limit, ps):
    points = Points(limit)
    points.extend(to_points(ps))

    assert(len(points) <= limit)


@given(st.lists(st.tuples(st.floats(allow_nan=False), st.floats(allow_nan=False))))
def test_points_maxs(ps):
    points = Points()
    ps = to_points(ps)

    try:
        max_x1 = max(map(lambda p: p.x, ps))
    except ValueError:
        max_x1 = 0

    try:
        max_y1 = max(map(lambda p: p.y, ps))
    except ValueError:
        max_y1 = 0

    points.extend(ps)

    _, _, max_x2, max_y2 = points.bounds()

    assert(max_x1 == max_x2)
    assert(max_y1 == max_y2)


@given(st.lists(st.tuples(st.floats(allow_nan=False), st.floats(allow_nan=False))))
def test_points_mins(ps):
    points = Points()
    ps = to_points(ps)

    try:
        min_x1 = min(map(lambda p: p.x, ps))
    except ValueError:
        min_x1 = 0

    try:
        min_y1 = min(map(lambda p: p.y, ps))
    except ValueError:
        min_y1 = 0

    points.extend(ps)

    min_x2, min_y2, _, _ = points.bounds()

    assert(min_x1 == min_x2)
    assert(min_y1 == min_y2)


@given(st.lists(st.tuples(st.floats(allow_nan=False), st.floats(allow_nan=False))))
def test_points_nothing_lost(ps):
    points = Points()
    ps = to_points(ps)

    points.extend(ps)

    assert(set(ps) == set(points.points()))

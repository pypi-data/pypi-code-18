

import re
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
import pytz


UTC = pytz.utc
CET = pytz.timezone("Europe/Berlin")


"""
@pytest.mark.parametrize("input_time,rel_time,output_time", [
    # CEST
    (datetime(2016, 10, 30, 2, 30),        "-1h@h",         datetime(2016, 10, 30, 1, 0)),
    (datetime(2016, 10, 30, 2, 30),        "@h",            datetime(2016, 10, 30, 2, 0)),
])
def test_snap_tz_wintertime_01(input_time, rel_time, output_time):
    assert snap_tz(input_time, rel_time, CET) == output_time


@pytest.mark.parametrize("input_time,rel_time,output_time", [
    # CET
    (datetime(2016, 10, 30, 3, 30),        "-1h@h",         datetime(2016, 10, 30, 2, 0)),
    (datetime(2016, 10, 30, 3, 30),        "@h",            datetime(2016, 10, 30, 3, 0)),
])
def test_snap_tz_wintertime_02(input_time, rel_time, output_time):
    assert snap_tz(input_time, rel_time, CET) == output_time
"""


def apply_to(dttm):
    unit = "hours"
    mult = -1
    num = 1
    return dttm + relativedelta(**{unit: mult * num})


def with_tz_apply_to_original(dttm, timezone):
    as_loc = timezone.localize(dttm)
    print "as_loc  : %s" % as_loc
    as_utc = as_loc.astimezone(UTC)
    print "as_utc  : %s" % as_utc
    new_dt = apply_to(as_utc)
    print "new_dt  : %s" % new_dt
    new_loc = new_dt.astimezone(timezone)
    print "new_loc : %s" % new_loc
    return new_loc.replace(tzinfo=None)  # no timezone info


def with_tz_apply_to(dttm, timezone):
    as_loc = timezone.localize(dttm, is_dst=True)
    print "as_loc  : %s" % as_loc
    # as_utc = as_loc.astimezone(UTC)
    # print "as_utc  : %s" % as_utc
    # new_dt = apply_to(as_utc)
    # print "new_dt  : %s" % new_dt
    # new_loc = new_dt.astimezone(timezone)
    # print "new_loc : %s" % new_loc
    new_loc = timezone.normalize(apply_to(as_loc))
    print "new_loc : %s" % new_loc
    return new_loc.replace(tzinfo=None)  # no timezone info


def main():
    dt01 = datetime(2016, 10, 30, 2, 30)
    # dt01 = datetime(2016, 10, 30, 3, 30)
    print dt01
    print

    print "original"
    res = with_tz_apply_to_original(dt01, CET)

    print
    print res

    print "new"
    res = with_tz_apply_to(dt01, CET)

    print
    print res


if __name__ == "__main__":
    main()

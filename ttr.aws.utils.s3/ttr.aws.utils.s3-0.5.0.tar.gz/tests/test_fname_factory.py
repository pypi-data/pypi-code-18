import dateutil.parser
from ttr.aws.utils.s3.saver import FnameFactory
import pytest


def get_last_modified_scenarios():
    plan = [["buck/k/n.json:1234aaa:2017-05-15T20:25:07Z",
             "n.2017-05-15T20_25_07Z.json"],
            ["buck/d.json:1234aaa:1970-01-01T00:00:00Z",
             "d.1970-01-01T00_00_00Z.json"],
            ]
    for objver, expected in plan:
        obj, version_id, dtstr = objver.split(":", 2)
        bucket_name, key_name = obj.split("/", 1)
        dt = dateutil.parser.parse(dtstr)
        objverdct = {"LastModified": dt, "VersionId": version_id}
        yield bucket_name, key_name, version_id, objverdct, expected


@pytest.mark.parametrize("scenario", list(get_last_modified_scenarios()))
def test_last_modified(scenario):
    bucket_name, key_name, version_id, objdict, expected = scenario
    fname_factory = FnameFactory().last_modified
    fname = fname_factory(bucket_name, key_name, version_id, objdict)
    assert fname == expected


def get_version_id_scenarios():
    plan = [["buck/k/n.json:1234aaa:2017-05-15T20:25:07Z",
             "n.1234aaa.json"],
            ["buck/d.json:1234aaa:1970-01-01T00:00:00Z",
             "d.1234aaa.json"],
            ]
    for objver, expected in plan:
        obj, version_id, dtstr = objver.split(":", 2)
        bucket_name, key_name = obj.split("/", 1)
        dt = dateutil.parser.parse(dtstr)
        objverdct = {"LastModified": dt, "VersionId": version_id}
        yield bucket_name, key_name, version_id, objverdct, expected


@pytest.mark.parametrize("scenario", list(get_version_id_scenarios()))
def test_version_id(scenario):
    bucket_name, key_name, version_id, objdict, expected = scenario
    fname_factory = FnameFactory().version_id
    fname = fname_factory(bucket_name, key_name, version_id, objdict)
    assert fname == expected

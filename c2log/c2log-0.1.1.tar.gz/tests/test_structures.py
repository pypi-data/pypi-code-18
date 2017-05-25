import datetime

from c2log.structures import FixedSplit
from c2log.structures import FixedWorkoutMeta
from c2log.structures import IntervalSplit
from c2log.structures import IntervalWorkoutMeta
from c2log.structures import VariableIntervalSplit


def assert_object_fields(fields, obj1, obj2):
    for f in fields:
        assert getattr(obj1, f) == getattr(obj2, f)


def test_user_struct(user):
    assert user.name == b'Ryan'

    assert user.lifetime_meters == 11912
    assert user.interval_rest_distance == 177
    assert user.num_workouts == 7


def test_fixed_workout(just_row_with_splits_workout):
    workout = just_row_with_splits_workout

    expected_splits = [
        FixedSplit(
            split_duration=3424,
            heartrate=0,
            spm=21,
        ),
        FixedSplit(
            split_duration=1479,
            heartrate=0,
            spm=15,
        )
    ]
    expected_split_fields = ('split_duration', 'heartrate', 'spm')

    expected_metadata = FixedWorkoutMeta(
        record_id=150,
        split_size=1100,
        total_work_duration=4903,
    )
    expected_metadata_fields = (
        'record_id', 'split_size', 'total_work_duration'
    )

    assert workout.type == 1
    assert workout.split_count == 2
    assert workout.duration == 4903
    assert workout.record_size == 114
    assert workout.name == 1446
    assert workout.date == datetime.date(2016, 11, 7)
    assert workout.datetime == datetime.datetime(2016, 11, 7, 15, 16)

    assert_object_fields(
        expected_metadata_fields, expected_metadata, workout.metadata
    )

    for idx, split in enumerate(workout.splits):
        assert_object_fields(
            expected_split_fields, expected_splits[idx], split
        )


def test_fixed_distance_workout(fixed_distance_workout):
    workout = fixed_distance_workout

    expected_splits = [
        FixedSplit(
            split_duration=3193,
            heartrate=0,
            spm=20,
        ),
        FixedSplit(
            split_duration=3244,
            heartrate=0,
            spm=20,
        ),
        FixedSplit(
            split_duration=3207,
            heartrate=0,
            spm=21,
        ),
        FixedSplit(
            split_duration=3225,
            heartrate=0,
            spm=22,
        ),
        FixedSplit(
            split_duration=3205,
            heartrate=0,
            spm=22,
        )
    ]
    expected_split_fields = ('split_duration', 'heartrate', 'spm')

    expected_metadata = FixedWorkoutMeta(
        record_id=150,
        split_size=1100,
        total_work_duration=16073,
    )
    expected_metadata_fields = (
        'record_id', 'split_size', 'total_work_duration'
    )

    assert workout.type == 3
    assert workout.split_count == 5
    assert workout.duration == 5500
    assert workout.record_size == 210
    assert workout.name == 16073
    assert workout.date == datetime.date(2016, 5, 23)
    assert workout.datetime == datetime.datetime(2016, 5, 23, 20, 18)

    assert_object_fields(
        expected_metadata_fields, expected_metadata, workout.metadata
    )

    for idx, split in enumerate(workout.splits):
        assert_object_fields(
            expected_split_fields, expected_splits[idx], split
        )


def test_fixed_time_workout(fixed_time_workout):
    workout = fixed_time_workout

    expected_splits = [
        FixedSplit(
            split_duration=832,
            heartrate=0,
            spm=22,
        ),
        FixedSplit(
            split_duration=822,
            heartrate=0,
            spm=22,
        ),
        FixedSplit(
            split_duration=819,
            heartrate=0,
            spm=22,
        ),
        FixedSplit(
            split_duration=832,
            heartrate=0,
            spm=22,
        ),
        FixedSplit(
            split_duration=840,
            heartrate=0,
            spm=23,
        )
    ]
    expected_split_fields = ('split_duration', 'heartrate', 'spm')

    expected_metadata = FixedWorkoutMeta(
        record_id=150,
        split_size=2400,
        total_work_duration=12000,
    )
    expected_metadata_fields = (
        'record_id', 'split_size', 'total_work_duration'
    )

    assert workout.type == 5
    assert workout.split_count == 5
    assert workout.duration == 12000
    assert workout.record_size == 210
    assert workout.name == 4144
    assert workout.date == datetime.date(2016, 5, 5)
    assert workout.datetime == datetime.datetime(2016, 5, 5, 19, 58)

    assert_object_fields(
        expected_metadata_fields, expected_metadata, workout.metadata
    )

    for idx, split in enumerate(workout.splits):
        assert_object_fields(
            expected_split_fields, expected_splits[idx], split
        )


def test_fixed_time_interval_workout(fixed_time_interval_workout):
    workout = fixed_time_interval_workout

    expected_splits = [
        IntervalSplit(
            split_duration=2195,
            heartrate=0,
            rest_heartrate=0,
            spm=23,
        ),
        IntervalSplit(
            split_duration=2145,
            heartrate=0,
            rest_heartrate=0,
            spm=22,
        )
    ]
    expected_split_fields = (
        'split_duration', 'heartrate', 'rest_heartrate', 'spm'
    )

    expected_metadata = IntervalWorkoutMeta(
        record_id=152,
        num_splits=2,
        split_size=6000,
        interval_rest_time=120,
        total_work_duration=4341,
        total_rest_distance=33,
    )
    expected_metadata_fields = (
        'record_id', 'num_splits', 'split_size', 'interval_rest_time',
        'total_work_duration', 'total_rest_distance'
    )

    assert workout.type == 6
    assert workout.rest == 120
    assert workout.name == 4341
    assert workout.split_count == 2
    assert workout.duration == 6000
    assert workout.date == datetime.date(2016, 5, 7)
    assert workout.datetime == datetime.datetime(2016, 5, 7, 20, 39)
    assert workout.record_size == 116
    assert workout.index == 3

    assert_object_fields(
        expected_metadata_fields, expected_metadata, workout.metadata
    )

    for idx, split in enumerate(workout.splits):
        assert_object_fields(
            expected_split_fields, expected_splits[idx], split
        )


def test_fixed_distance_interval_workout(fixed_distance_interval_workout):
    workout = fixed_distance_interval_workout

    expected_splits = [
        IntervalSplit(
          split_duration=1372,
          heartrate=0,
          rest_heartrate=0,
          spm=22,
        ),
        IntervalSplit(
          split_duration=1332,
          heartrate=0,
          rest_heartrate=0,
          spm=22,
        ),
        IntervalSplit(
          split_duration=1314,
          heartrate=0,
          rest_heartrate=0,
          spm=22,
        ),
        IntervalSplit(
          split_duration=1260,
          heartrate=0,
          rest_heartrate=0,
          spm=23,
        ),
        IntervalSplit(
          split_duration=1442,
          heartrate=0,
          rest_heartrate=0,
          spm=21,
        ),
        IntervalSplit(
          split_duration=1376,
          heartrate=0,
          rest_heartrate=0,
          spm=22,
        )
    ]
    expected_split_fields = (
        'split_duration', 'heartrate', 'rest_heartrate', 'spm'
    )

    expected_metadata = IntervalWorkoutMeta(
        record_id=152,
        num_splits=6,
        split_size=500,
        interval_rest_time=120,
        total_work_duration=8095,
        total_rest_distance=107,
    )
    expected_metadata_fields = (
        'record_id', 'num_splits', 'split_size', 'interval_rest_time',
        'total_work_duration', 'total_rest_distance'
    )

    assert workout.type == 7
    assert workout.rest == 120
    assert workout.name == 8095
    assert workout.split_count == 6
    assert workout.duration == 500
    assert workout.date == datetime.date(2016, 11, 4)
    assert workout.datetime == datetime.datetime(2016, 11, 4, 17, 23)
    assert workout.record_size == 244
    assert workout.index == 1

    for idx, split in enumerate(workout.splits):
        assert_object_fields(
            expected_split_fields, expected_splits[idx], split
        )

    assert_object_fields(
        expected_metadata_fields, expected_metadata, workout.metadata
    )


def test_variable_interval(variable_interval_workout):
    workout = variable_interval_workout

    expected_splits = [
        VariableIntervalSplit(
            split_type=0,
            spm=23,
            work_interval_time=1291,
            work_interval_distance=500,
            heartrate=0,
            rest_heartrate=0,
            interval_rest_time=90,
            interval_rest_distance=14
        ),
        VariableIntervalSplit(
            split_type=0,
            spm=24,
            work_interval_time=1200,
            work_interval_distance=464,
            heartrate=0,
            rest_heartrate=0,
            interval_rest_time=90,
            interval_rest_distance=9
        ),
        VariableIntervalSplit(
            split_type=0,
            spm=24,
            work_interval_time=663,
            work_interval_distance=250,
            heartrate=0,
            rest_heartrate=0,
            interval_rest_time=60,
            interval_rest_distance=14
        )
    ]
    expected_split_fields = (
        'split_type', 'spm', 'work_interval_time', 'work_interval_distance',
        'heartrate', 'rest_heartrate', 'interval_rest_time',
        'interval_rest_distance'
    )

    expected_metadata = IntervalWorkoutMeta(
        record_id=154,
        num_splits=3,
        total_work_duration=3154,
        total_work_distance=1213
    )
    expected_metadata_fields = (
        'record_id', 'num_splits', 'total_work_duration', 'total_work_distance'
    )

    assert workout.type == 8
    assert workout.split_type == 1
    assert workout.split_count == 3
    assert workout.rest == 90
    assert workout.name == 1291
    assert workout.duration == 500
    assert workout.date == datetime.date(2017, 4, 14)
    assert workout.datetime == datetime.datetime(2017, 4, 14, 13, 57)
    assert workout.record_size == 196
    assert workout.index == 4

    for idx, split in enumerate(workout.splits):
        assert_object_fields(
            expected_split_fields, expected_splits[idx], split
        )

    assert_object_fields(
        expected_metadata_fields, expected_metadata, workout.metadata
    )

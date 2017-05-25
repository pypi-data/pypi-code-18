import pytest
from c2log.structures import BaseWorkout


class Meta:
    """Empty class to hold metadata values for testing"""


def test_fixed_time_workout_name():
    workout = BaseWorkout()
    workout.name = '3455'

    for workout_type in (1, 4, 5):
        workout.type = workout_type
        assert workout.workout_name == '0:05:45'


def test_fixed_distance_workout_name():
    workout = BaseWorkout()
    workout.name = '5500'

    for workout_type in (2, 3):
        workout.type = workout_type
        assert workout.workout_name == '5500m'


def test_fixed_time_interval_workout_name():
    workout = BaseWorkout()
    workout.type = 6
    workout.metadata = Meta()
    workout.metadata.split_size = 1200  # 2 minutes in tenths of a second
    workout.metadata.num_splits = 5
    workout.metadata.interval_rest_time = 600

    assert workout.workout_name == '5x2:00/1:00r'


def test_fixed_distance_interval_workout_name():
    workout = BaseWorkout()
    workout.type = 7
    workout.metadata = Meta()
    workout.metadata.split_size = 1100
    workout.metadata.num_splits = 5
    workout.metadata.interval_rest_time = 900

    assert workout.workout_name == '5x1100m/1:30r'


def test_variable_interval_workout_name():
    workout = BaseWorkout()
    workout.split_type = 1
    workout.type = 8
    workout.duration = 500
    workout.rest = 90
    workout.splits = (Meta(), (), ())
    workout.split_count = 3

    assert workout.workout_name == 'v500m/1:30r...3'

    workout.split_type = 0
    workout.splits[0].work_interval_time = 1200
    assert workout.workout_name == 'v2:00/1:30r...3'


def test_undefined_workout_name():
    workout = BaseWorkout()
    workout.type = -1

    assert workout.workout_name == 'undefined'


def test_pace_watts_calories():
    workout = BaseWorkout()
    workout.total_work_duration = 12000  # 20 minutes in tenths of a second
    workout.total_work_distance = 0
    assert workout.pace == 0.0

    workout.total_work_distance = 4137

    assert workout.pace == pytest.approx(0.290065)
    assert workout.watts == pytest.approx(114.7, .01)
    assert workout.calories == pytest.approx(694, .01)

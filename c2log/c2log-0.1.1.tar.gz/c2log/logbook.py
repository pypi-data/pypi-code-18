import struct

from c2log.structures import FixedWorkout
from c2log.structures import IntervalWorkout
from c2log.structures import User
from c2log.structures import VariableIntervalWorkout


def interleave_workouts(directory):
    """
    Create one interleaved file given a directory of log files

    Workout data is spread across two different files. The records
    in the first contain metadata and offsets into the second file
    where split data can be found.

    To ease parsing of these files they can be interleaved so that
    the splits for a workout immediately follow its metadata.

    :param directory: Path to log files.
    :returns: List of workout and split data
    """

    with open('{}/LogDataAccessTbl.bin'.format(directory), 'rb') as f:
        # LogAccessTbl.bin contains a 32 byte record for each workout.
        record = f.read(32)
        while record[0:2] != b'\xff\xff':
            offset = struct.unpack('<16H', record)[8]
            size = struct.unpack('<16H', record)[12]

            # LogDataStorage.bin contains additional workout metadata and
            # all the interval data. The size of this metadata plus intervals
            # is found at bytes 25-26 in the data above.

            intervals = []
            with open('{}/LogDataStorage.bin'.format(directory), 'rb') as f2:
                f2.seek(offset)
                interval_data = f2.read(size)
                intervals.append(interval_data)

            result = b''.join([record] + intervals)
            yield result

            record = f.read(32)


class LogBook:
    """
    """

    workout_map = {
        1: FixedWorkout,
        2: FixedWorkout,
        3: FixedWorkout,
        4: FixedWorkout,
        5: FixedWorkout,
        6: IntervalWorkout,
        7: IntervalWorkout,
        8: VariableIntervalWorkout
    }

    def __init__(self, workouts=None, user=None):
        self.workouts = workouts
        self.user = user

    def _workouts(self, workout_data):
        output = []

        for workout in workout_data:
            workout_type = workout[1]
            workout_class = self.workout_map[workout_type]

            output.append(workout_class.from_data(workout))

        return output

    @classmethod
    def from_directory(cls, directory):
        """
        Creates a new logbook object from a set of log files

        :param directory: Path to log files
        :returns: :class:`LogBook` instance
        """
        obj = cls()
        obj.directory = directory

        obj.workouts = obj._workouts(interleave_workouts(directory))

        data = b''
        with open('{}/UserStatic.bin'.format(directory), 'rb') as f:
            data += f.read()

        with open('{}/UserDynamic.bin'.format(directory), 'rb') as f:
            data += f.read(74)

        obj.user = User.from_data(data)

        return obj

    @property
    def lifetime_meters(self):
        """
        Total number of meters in this logbook

        Lifetime meters includes meters rowed during workouts
        and meters accrued during interval rest times.

        :returns: int
        """
        return self.user.lifetime_meters + self.user.interval_rest_distance

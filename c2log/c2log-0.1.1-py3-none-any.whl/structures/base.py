import datetime

from suitcase.fields import BitField
from suitcase.fields import BitNum
from suitcase.fields import Magic
from suitcase.fields import SubstructureField
from suitcase.fields import UBInt16
from suitcase.fields import UBInt32
from suitcase.fields import UBInt8
from suitcase.fields import ULInt16
from suitcase.structure import Structure

from c2log.fields import UBInt16Sequence


class ULDate(Structure):
    """
    16-bit unsigned little-endian date

    This is a bitfield with the following structure:
        year:  bits 1-7
        day:   bits 8-12
        month: bits 13-16
    """
    date = BitField(
        16,
        ULInt16(),
        year=BitNum(7),
        day=BitNum(5),
        month=BitNum(4),
    )


class UBDate(Structure):
    """
    16-bit unsigned big-endian date

    This is a bitfield with the following structure:

        year:  bits 1-7
        day:   bits 8-12
        month: bits 13-16
    """
    date = BitField(
        16,
        UBInt16(),
        year=BitNum(7),
        day=BitNum(5),
        month=BitNum(4),
    )


class UBTime(Structure):
    """
    16-bit unsigned big-endian timestamp

    This is a bitfield with the following structure:
        hours:   bits 1-8
        minutes: bits 9-16
    """
    time = BitField(
        16,
        UBInt16(),
        hours=BitNum(8),
        minutes=BitNum(8)
    )


class BaseWorkout:
    """Interface for all workouts.

    There are three different types of workouts.
    Among each of these workouts there are different
    fields, e.g.some have interval_rest, some don't.

    This class provides a single, high-level interface to the
    different workout types. It also provides convenience
    functions for many fields.
    """

    @property
    def date(self):
        """
        Converts a 16 bit date value to datetime.date

        :returns: datetime.date instance
        """
        return datetime.date(
            2000 + self.date_struct.date.year,
            self.date_struct.date.month,
            self.date_struct.date.day
        )

    @property
    def datetime(self):
        """
        Converts a 32 bit datetime value to datetime.datetime

        :returns: datetime.datetime instance
        """
        timestamp = self.metadata.header
        return datetime.datetime(
            2000 + timestamp.date_struct.date.year,
            timestamp.date_struct.date.month,
            timestamp.date_struct.date.day,
            timestamp.time_struct.time.hours,
            timestamp.time_struct.time.minutes
        )

    @property
    def pace(self):
        """Pace in sec/meter

        Pace is calculated by dividing the total workout distance
        by the workout duration.

        :returns: float
        """
        if self.total_work_distance != 0:
            return (self.total_work_duration / 10) / self.total_work_distance
        return 0.0

    @property
    def watts(self):
        """
        Power generated in watts

        :returns: float
        """
        return 2.8 / (self.pace ** 3)

    @property
    def calories(self):
        """
        Calculates calories/hour

        :returns: float
        """
        return ((2.8 / ((self.pace ** 3))) * (4 * 0.8604)) + 300

    def _format_time(self, seconds, include_hours=False):
        sec = int(seconds) / 10

        minutes, seconds = divmod(sec, 60)
        hours, minutes = divmod(minutes, 60)
        hours, minutes, seconds = int(hours), int(minutes), int(seconds)

        if hours > 0 or include_hours:
            hours = str(hours) + ":"
            minutes = str(minutes).zfill(2)
        else:
            hours = ""
            minutes = int(minutes)

        return '{}{}:{:02d}'.format(hours, minutes, seconds)

    @property
    def workout_name(self):
        """
        Derives workout name.

        The format of workout name varies by workout type.
        All names seems to be derived from the workout duration
        which is either the workout time in tenths of a second
        or the workout distance in meters.

        :returns: Dervied workout name
        """
        if self.type in (1, 4, 5):
            name = self._format_time(self.name, True)
        elif self.type in (2, 3):
            name = '{}m'.format(self.name)
        elif self.type == 6:
            name = '{}x{}'.format(
                self.metadata.num_splits,
                self._format_time(self.metadata.split_size)
            )
            rest = ''
            if self.metadata.interval_rest_time:
                rest = '/{}r'.format(
                    self._format_time(self.metadata.interval_rest_time)
                )

            name = name + rest
        elif self.type == 7:
            name = '{}x{}m'.format(
                self.metadata.num_splits, self.metadata.split_size
            )
            rest = ''
            if self.metadata.interval_rest_time:
                rest = '/{}r'.format(
                    self._format_time(self.metadata.interval_rest_time)
                )

            name = name + rest
        elif self.type in (8, 9):
            name = 'v'
            if self.split_type == 1:
                name += str(self.duration) + 'm/'
            else:
                name += '{}/'.format(
                    self._format_time(self.splits[0].work_interval_time)
                )

            if len(self.splits) >= 2:
                # Rest time is stored as seconds instead of tenths of a second
                # as every other time related field is...
                name += self._format_time(self.rest * 10)

            name += 'r...' + str(self.split_count)
        else:
            name = 'undefined'

        return name


class WorkoutMetaHeader(Structure):
    """
    Header data shared by all workouts

    Each workout record in :doc:`/file_formats/logdatastorage.bin`
    has an 18 byte header followed by the split data.
    """
    header = Magic(b'\x95')
    type = UBInt8()
    tbd0 = UBInt16()
    serial_number = UBInt32()

    # Can't use the Date substructure here because date
    # is big-endian here.
    date_struct = SubstructureField(UBDate)
    time_struct = SubstructureField(UBTime)
    user_id = UBInt16()
    tbd1 = UBInt16Sequence(2)

from suitcase.structure import Structure
from suitcase.fields import FieldArray
from suitcase.fields import LengthField
from suitcase.fields import Magic
from suitcase.fields import SubstructureField
from suitcase.fields import UBInt16
from suitcase.fields import UBInt32
from suitcase.fields import UBInt8
from suitcase.fields import ULInt16

from c2log.fields import UBInt16Sequence
from c2log.structures import BaseWorkout
from c2log.structures import ULDate
from c2log.structures import WorkoutMetaHeader


class IntervalWorkoutMeta(Structure):
    header = SubstructureField(WorkoutMetaHeader)

    record_id = UBInt8()

    num_splits = UBInt8()
    split_size = UBInt16()
    interval_rest_time = UBInt16()
    total_work_duration = UBInt32()
    total_rest_distance = UBInt16()

    tbd = UBInt16Sequence(11)


class IntervalSplit(Structure):
    """
    Each split record is 32 bytes long
    """

    split_duration = UBInt16()
    heartrate = UBInt8()
    rest_heartrate = UBInt8()
    spm = UBInt8()
    tbd = UBInt8()
    tbd1 = UBInt16Sequence(13)


class IntervalWorkout(BaseWorkout, Structure):
    """
    Interval workouts

    This structure covers fixed time and fixed distance intervals.

    These workouts have two extra bytes in the metadata and some
    of the values are in different locations compared to
    :class:`.FixedWorkout`.

    Types 6 and 7
    """
    header = Magic(b'\xf0')
    type = UBInt8()
    rest = ULInt16()
    name = ULInt16()
    tbd0 = UBInt16()
    date_struct = SubstructureField(ULDate)
    tbd1 = UBInt16()
    split_count = LengthField(ULInt16())
    duration = UBInt16()
    record_offset = UBInt16()
    tbd2 = UBInt16()
    tbd3 = UBInt16()
    tbd4 = UBInt16()
    record_size = ULInt16()
    index = ULInt16()
    tbd5 = UBInt16Sequence(2)

    metadata = SubstructureField(IntervalWorkoutMeta)
    splits = FieldArray(IntervalSplit)

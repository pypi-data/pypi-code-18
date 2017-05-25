from suitcase.structure import Structure
from suitcase.fields import BitField
from suitcase.fields import BitNum
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


class FixedWorkoutMeta(Structure):
    """
    Metadata for fixed workouts

    This metadata includes the shared header that all
    workout types have as well as information about
    the total distance and duration of the workout.
    """
    header = SubstructureField(WorkoutMetaHeader)

    record_id = UBInt8()
    tbd = Magic(b'\x00')

    total_work_duration = UBInt32()
    total_work_distance = UBInt32()

    spm = UBInt8()
    split_info = BitField(
        8,
        UBInt8(),
        split_type=BitNum(4),
        num_splits=BitNum(4)
    )

    split_size = UBInt16()
    tbd3 = UBInt16Sequence(4)

    # This sequence is the same across all records
    # but differs by device
    tbd4 = UBInt16Sequence(4)
    tbd5 = UBInt16Sequence(1)


class FixedSplit(Structure):
    """
    Each split record is 32 bytes long
    """

    split_duration = UBInt16()
    heartrate = UBInt8()
    spm = UBInt8()
    tbd = UBInt16Sequence(14)


class FixedWorkout(BaseWorkout, Structure):
    """
    Fixed workouts are types 0 - 5.

    This structure covers free row, fixed time, and fixed distance
    workouts.
    """
    header = Magic(b'\xf0')
    type = UBInt8()
    rest = Magic(b'\x00\x00')  # Fixed workouts don't have rest periods
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

    metadata = SubstructureField(FixedWorkoutMeta)
    splits = FieldArray(FixedSplit)

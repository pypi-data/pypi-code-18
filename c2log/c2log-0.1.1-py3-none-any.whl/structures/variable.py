from suitcase.structure import Structure
from suitcase.fields import FieldArray
from suitcase.fields import Magic
from suitcase.fields import SubstructureField
from suitcase.fields import UBInt16
from suitcase.fields import UBInt32
from suitcase.fields import UBInt8
from suitcase.fields import UBInt8Sequence
from suitcase.fields import ULInt16
from suitcase.fields import ULInt8

from c2log.fields import UBInt16Sequence
from c2log.structures import BaseWorkout
from c2log.structures import ULDate
from c2log.structures import WorkoutMetaHeader


class VariableIntervalWorkoutMeta(Structure):
    header = SubstructureField(WorkoutMetaHeader)

    record_id = UBInt8()
    num_splits = UBInt8()
    total_work_duration = UBInt32()
    total_work_distance = UBInt32()
    tbd = UBInt16Sequence(12)

    split_size = 0


class VariableIntervalSplit(Structure):
    """
    Variable interval splits are 48 bytes long
    """

    split_type = ULInt8()
    spm = UBInt8()
    work_interval_time = UBInt32()
    work_interval_distance = UBInt32()
    heartrate = UBInt8()
    rest_heartrate = UBInt8()
    interval_rest_time = UBInt16()
    interval_rest_distance = UBInt16()
    tbd = UBInt8Sequence(32)


class VariableIntervalWorkout(BaseWorkout, Structure):
    """
    Variable Interval workouts

    This structure covers variable intervals which are
    type 8.
    """
    header = Magic(b'\xf0')
    type = UBInt8()
    rest = ULInt16()
    name = ULInt16()
    tbd0 = UBInt16()
    date_struct = SubstructureField(ULDate)
    tbd1 = UBInt16()
    split_type_and_count = ULInt16()
    duration = UBInt16()
    record_offset = UBInt16()
    tbd2 = UBInt16()
    tbd3 = UBInt16()
    tbd4 = UBInt16()
    record_size = ULInt16()
    index = ULInt16()
    tbd5 = UBInt16Sequence(2)

    metadata = SubstructureField(VariableIntervalWorkoutMeta)
    splits = FieldArray(VariableIntervalSplit)

    @property
    def split_type(self):
        # This split_type is only used to generate the workout name.
        # It is the type of the first interval.
        return self.split_type_and_count >> 7

    @property
    def split_count(self):
        return len(self.splits)

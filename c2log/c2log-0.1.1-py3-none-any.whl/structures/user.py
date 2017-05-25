from suitcase.fields import UBInt16
from suitcase.fields import UBInt32
from suitcase.structure import Structure

from c2log.fields import FixedLengthString
from c2log.fields import UBInt16Sequence


class User(Structure):
    """
    Structure containing information about the owner of this logbook.

    This structure is created by combining the data found in
    :doc:`/file_formats/userstatic.bin` and
    :doc:`/file_formats/userdynamic.bin`.

    The name is stored in the binary file as 6 bytes regardless
    of the actual length of the name. The FixedLengthString field type
    strips the extra '\0' characters from the name.
    """
    tbd1 = UBInt16()
    name = FixedLengthString(6)
    tbd2 = UBInt16Sequence(27)

    lifetime_meters = UBInt32()
    interval_rest_distance = UBInt32()

    total_time = UBInt32()
    num_workouts = UBInt16()

    tbd3 = UBInt16Sequence(28)

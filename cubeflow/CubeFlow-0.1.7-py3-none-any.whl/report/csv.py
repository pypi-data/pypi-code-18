from typing import Sequence
from itertools import cycle
from cubeflow.report import Report
from cubeflow.cube import T, CubeGrid


class CSVReport(Report[T]):
    """
    Provides a means for storing the course of the simulation as csv files, one
    file for each simulation step. You have to specify a converter if your data
    cells do not use MetaCell as metaclass.
    """

    def __init__(self, fileprefix: str, convert=lambda x: x.values(), headline=None) -> None:
        """
        Constructs a new *CSVReport* instance. All resulting csv files, one per simulation step performed,
        are stored under the name **fileprefix.csv.i** within the current directory with i being the simulation step
        number. The default converter is suitable for all cell types with metaclass *MetaCell*. A translation by 0.5
        regarding any dimension is performed to center the simulation values within the cell. To change this behaviour
        set the delta attribute to an appropriate value or None, if no translation is desired.
        :param fileprefix: Name prefix of all created csv files.
        :param convert: Converter that transforms all cells to the csv values. If *CellType* does not have metaclass
        *MetaCell*, headline must also be specified.
        :param headline: Alternative headline for the csv file header. Usually not required (see above).
        """
        super().__init__(fileprefix)
        self._converter = convert
        self._headline = headline
        self.delta = cycle((0.5,))

    def __call__(self, grid: CubeGrid[T], t: float) -> None:
        """
        Creates a csv file from a grid, usually the current grid configuration of the simulation. 
        :param grid: Grid which cell values will be stored in the csv file. 
        :param t: The time connected to the current grid.
        :return: Nothing
        """
        with open("{0}.csv.{1}".format(self._prefix, self._index), 'w') as out:
            if not self._headline:
                self._headline = list("xyzuvw"[0:grid.dimension])
                self._headline.append('t')
                self._headline.extend(grid[0].names())
            out.write(','.join(self._headline) + '\n')
            for (coord, cell) in grid.coordinate_system:
                cell_data = list(self.move(coord))
                cell_data.append(t)
                cell_data.extend(self._converter(cell))
                out.write(','.join(map(str, cell_data)))
                out.write('\n')
            self._index += 1

    def move(self, coord: Sequence[int]) -> Sequence[float]:
        """
        Performs a translation of all cell coordinates by self.delta, if specified (not None).
        :param coord: Sequence of integer coordinates of the cell. 
        :return: Translated coordinates.
        """
        if self.delta is None:
            return coord
        return tuple((c+d for (c, d) in zip(coord, self.delta)))

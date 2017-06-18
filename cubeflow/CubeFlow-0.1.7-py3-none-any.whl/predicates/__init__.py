from typing import Any, Sequence, Callable
from cubeflow.cube import CubeGrid, T


class _Predicate:
    """
    Base class for all predicates defined in *CubeFlow*, should not be used outside *CubeFlow*.
    """
    def __init__(self, *sub_predicates: Sequence[Any]) -> None:
        self._sub_predicates = sub_predicates if sub_predicates else None

    def __call__(self, grid: CubeGrid[T]) -> bool:
        if self._sub_predicates:
            return all(predicate(grid) for predicate in self._sub_predicates)
        else:
            return False

    def __add__(self, other):
        return _Predicate(self, other)


class Predicate(_Predicate):
    """
    Base class for all custom type predicates defined by the user.
    """
    def __init__(self) -> None:
        super().__init__(self)

    def __call__(self, grid: CubeGrid[T]) -> bool:
        """
        Evaluates a grid according to the predicate.
        :param grid: Grid to be evaluated.
        :return: True if the predicate is satisfied entirely, False otherwise.
        """
        return _Predicate.__call__(self, grid)


class CustomPredicate(Predicate):
    """
    Predicate that evaluates to true if a given function is true for any cell within a grid.
    """
    def __init__(self, check: Callable[[T], bool]):
        """
        Constructs a new *CustomPredicate* instance.
        :param check: Evaluation function that takes a grid cell and returns a boolean.
        """
        self._check = check

    def __call__(self, grid: CubeGrid[T]) -> bool:
        """
        Checks if the given cell predicate is true for all cells.
        :param grid: The grid which cells should be evaluated.
        :return: True if any cell fulfills the given predicate function, False otherwise.
        """
        return all(self._check(cell) for cell in grid.grid)

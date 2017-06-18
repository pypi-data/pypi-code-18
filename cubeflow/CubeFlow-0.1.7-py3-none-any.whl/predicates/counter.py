from cubeflow.predicates import Predicate


class Counter(Predicate):
    """
    Predicate that yields True for a certain amount of checks. Used for simulations that should abort after a specified
    amount of simulation steps. Useful in a combined predicate to define a maximum number of steps for the simulation.  
    >>> pred = Counter(30) + Counter(2)
    >>> pred(None)
    True
    >>> pred(None)
    True
    >>> pred(None)
    False
    """

    def __init__(self, value: int) -> None:
        """
        Constructs a new *Counter* instance.
        :param value: Non-negative number to be used for the descending counter.
        """
        super().__init__()
        self._value = value

    def __call__(self, _) -> bool:
        """
        Decreases the counter by one and checks if its value is still non-negative.
        :param _: Usually a grid, since counters do not have to take the grid into account, this parameter is not used
        and only present for the sake of interface.
        :return: True if counter has not reached zero, False otherwise.
        """
        self._value -= 1
        return self._value >= 0

import typing
import plinq.utils as utils


class OrderOption(object):
    """
    Stores ordering related information
    """
    def __init__(self, key_selector: typing.Callable=None, reverse: bool=False):
        utils.check_callable(key_selector, name="key_selector", optional=True)
        self.key_selector = key_selector
        self.reverse = reverse


class OrderedIterable(object):
    """
    Handles multi-ordered iterables in a lazy way
    """
    def __init__(self, iterable: typing.Iterable, order_option: OrderOption):
        utils.check_iterable(iterable, name="iterable")
        if not isinstance(order_option, OrderOption):
            raise TypeError("Parameter 'order_option' must be an OrderOption object")
        self._iterable = iterable
        self._order_options = [order_option]

    def __iter__(self):
        return OrderedIterator(self._iterable, self._order_options)

    def add_order(self, order_option: OrderOption):
        self._order_options.insert(0, order_option)


class OrderedIterator(object):
    """
    Handles multi-ordered iterables in a lazy way. Ordering will only happen when the first item is fetched
    """
    def __init__(self, iterable: typing.Iterable, order_options: typing.List[OrderOption]) -> None:
        utils.check_iterable(iterable, name="iterable")
        self._iterable = iterable
        self._order_options = order_options
        self._iterator = None  # type: typing.Iterator

    def __iter__(self):
        return self

    def __next__(self):
        if self._iterator is None:
            iterable = self._iterable
            for order_option in self._order_options:
                iterable = sorted(iterable, key=order_option.key_selector, reverse=order_option.reverse)
            self._iterator = iter(iterable)
        return self._iterator.__next__()

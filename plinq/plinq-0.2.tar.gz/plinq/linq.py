import typing
import collections
from plinq.generator_iterable import GeneratorIterable

# TODO: Add operators like min_item and max_item, which needs an optional selector, and returns the item itself
#       which is the smallest, not just the item returned by selector. An easy way to select the youngest person e.g.


# C# LINQ operators   Python LINQ operators
# -----------------------------------------
# Filtering Operators
# -----------------------------------------
# Where               where
# OfType              of_type
# -----------------------------------------
# Join Operators
# -----------------------------------------
# Join                join
# GroupJoin           group_join
# Zip                 zip
# -----------------------------------------
# Projection Operators
# -----------------------------------------
# Select              select
# SelectMany          select_many
# -----------------------------------------
# Sorting Operators
# -----------------------------------------
# OrderBy             order_by
# OrderByDescending   order_by_descending
# ThenBy              *None*
# ThenByDescending    *None*
# Reverse             reverse
# -----------------------------------------
# Grouping Operators
# -----------------------------------------
# GroupBy             group_by
# ToLookUp            NA
# -----------------------------------------
# Conversions Operators
# -----------------------------------------
# AsEnumerable        NA
# AsQueryable         NA
# Cast                NA
# ToArray             NA
# ToDictionary        to_dictionary
# ToList              to_list
# -----------------------------------------
# Concatenation Operators
# -----------------------------------------
# Concat              concat
# -----------------------------------------
# Aggregation Operators
# -----------------------------------------
# Aggregate           aggregate
# Average             average
# Count               count
# LongCount           NA
# Max                 max
# Min                 min
# Sum                 sum
# -----------------------------------------
# Quantifier Operators
# -----------------------------------------
# All                 all
# Any                 any
# Contains            contains
# -----------------------------------------
# Partition Operators
# -----------------------------------------
# Skip                skip
# SkipWhile           skip_while
# Take                take
# TakeWhile           take_while
# -----------------------------------------
# Generation Operators
# -----------------------------------------
# DefaultIfEmpty      plinq.default_if_empty
# Empty               plinq.empty
# Range               plinq.from_range
# Repeat              plinq.repeat
# -----------------------------------------
# Set Operators
# -----------------------------------------
# Distinct            distinct
# Except              exclude
# Intersect           intersect
# Union               union
# -----------------------------------------
# Equality Operators
# -----------------------------------------
# SequenceEqual       sequence_equal
# -----------------------------------------
# Element Operators
# -----------------------------------------
# ElementAt           element_at
# ElementAtOrDefault  element_at_or_default
# First               first
# FirstOrDefault      first_or_default
# Last                last
# LastOrDefault       last_or_default
# Single              single
# SingleOrDefault     single_or_default

# TODO: Make it more pythonic by using some of the language features.
#       E.g.: result_selector in zip() should be optional, and we could just return a tuple and so on
class Linq(object):
    def __init__(self, iterable: typing.Iterable) -> None:
        self._check_iterable(iterable, name="iterable")
        self._iterable = iterable

    def __iter__(self) -> typing.Iterator:
        return iter(self._iterable)

    #
    # Filtering Operators
    #

    def where(self, predicate: typing.Callable) -> "Linq":
        """
        Implements the where linq operator
        :param predicate: A callable object capable of handling two positional arguments, item and index (in that order)
                          and returns a boolean
        :return: A new Linq object, which will only return items, satisfying the given predicate
        """
        self._check_callable(predicate, name="predicate")

        def where_generator():
            for index, item in enumerate(self._iterable):
                if predicate(item, index):
                    yield item
        return Linq(GeneratorIterable(where_generator))

    def of_type(self, of_type: typing.Type) -> "Linq":
        """
        Implements the of type linq operator
        :param of_type: The type of the items to return from the current Linq
        :return: A new Linq object which contains only the items of the wanted type
        """
        if not isinstance(of_type, type):
            raise TypeError("Parameter 'of_type' must be a type")

        def of_type_generator():
            for item in self._iterable:
                if isinstance(item, of_type):
                    yield item
        return Linq(GeneratorIterable(of_type_generator))

    #
    # Join Operators
    #

    def join(self, inner_iterable: typing.Iterable,
             outer_key_selector: typing.Callable,
             inner_key_selector: typing.Callable,
             result_selector: typing.Callable) -> "Linq":
        """
        Implements the join linq operator
        :param inner_iterable The other iterable to join the Linq object with
        :param outer_key_selector A callable to obtain the key from an item in the current range
        :param inner_key_selector A callable to obtain the key from an item in the inner_iterable
        :param result_selector A callable to obtain the return value from the matching items
                               All matching items passed as the second argument
        :return A new Linq object with the items returned by the result_selector
        """
        self._check_iterable(inner_iterable, name="inner_iterable")
        self._check_callable(outer_key_selector, name="outer_key_selector")
        self._check_callable(inner_key_selector, name="inner_key_selector")
        self._check_callable(result_selector, name="result_selector")

        def join_generator():
            for outer_item in self._iterable:
                # Get the outer key
                outer_key = outer_key_selector(outer_item)
                inner_items = []
                # Try to find matching elements from the inner iterator
                for inner_item in inner_iterable:
                    inner_key = inner_key_selector(inner_item)
                    if inner_key == outer_key:
                        inner_items.append(inner_item)
                # Go through all the find matching elements and invoke result selector with them and the outer item
                for inner_item in inner_items:
                    yield result_selector(outer_item, inner_item)
        return Linq(GeneratorIterable(join_generator))

    def group_join(self, inner_iterable: typing.Iterable,
                   outer_key_selector: typing.Callable,
                   inner_key_selector: typing.Callable,
                   result_selector: typing.Callable) -> "Linq":
        """
        Implements the group join linq operator
        :param inner_iterable The other iterable to group join the Linq object with
        :param outer_key_selector A callable to obtain the key from an item in the current range
        :param inner_key_selector A callable to obtain the key from an item in the inner_iterable
        :param result_selector A callable to obtain the return value from the matching items
                               All matching items are passed as a list in the second parameter
        :return A new Linq object with the items returned by the result_selector
        """
        self._check_iterable(inner_iterable, name="inner_iterable")
        self._check_callable(outer_key_selector, name="outer_key_selector")
        self._check_callable(inner_key_selector, name="inner_key_selector")
        self._check_callable(result_selector, name="result_selector")

        def group_join_generator():
            for outer_item in self._iterable:
                # Get the outer key
                outer_key = outer_key_selector(outer_item)
                inner_items = []
                # Try to find matching elements from the inner iterator
                for inner_item in inner_iterable:
                    inner_key = inner_key_selector(inner_item)
                    if inner_key == outer_key:
                        inner_items.append(inner_item)
                # If there are matching items call the result selector and yield the result
                if len(inner_items) != 0:
                    yield result_selector(outer_item, inner_items)
        return Linq(GeneratorIterable(group_join_generator))

    def zip(self, inner_iterable: typing.Iterable, result_selector: typing.Callable) -> "Linq":
        """
        Implements the zip linq operator
        :param inner_iterable: The other iterable to zip the Linq object with
        :param result_selector: A callable to obtain the return value for pairs
                                The first parameter is the item from the current range,
                                the second parameter is the item from the inner_iterable
        :return: A new Linq object containing the items returned by result_selector.
        """
        self._check_iterable(inner_iterable, name="inner_iterable")
        self._check_callable(result_selector, name="result_selector")

        def zip_generator():
            for outer_item, inner_item in zip(self._iterable, inner_iterable):
                yield result_selector(outer_item, inner_item)
        return Linq(GeneratorIterable(zip_generator))

    #
    # Projection Operators
    #

    def select(self, selector: typing.Callable) -> "Linq":
        """
        Implements the select linq operator
        :param selector: A callable object capable of handling two positional arguments, item and index (in that order)
                         and returns a converted value (which can be even None)
        :return: A new Linq object, which will convert every item in the original iterable
        """
        self._check_callable(selector, name="selector")

        def select_generator():
            for index, item in enumerate(self._iterable):
                yield selector(item, index)
        return Linq(GeneratorIterable(select_generator))

    def select_many(self, collection_selector: typing.Callable, result_selector: typing.Callable=None) -> "Linq":
        """
        Implements the select many linq operator
        :param collection_selector: A callable to obtain the collection for the item in the current Linq
        :param result_selector: Optional callable to obtain the final result, from the item in the current range
                                and the item from returned collection by collection_selector
        :return: A new Linq object containing all the items from the returned collections by collection_selector
                 If result selector is specified, the items will be the returned values of result_selector
        """
        self._check_callable(collection_selector, name="collection_selector")
        self._check_callable(result_selector, name="result_selector", optional=True)

        def select_many_generator():
            for index, item in enumerate(self._iterable):
                # Get the collection, based on the item
                collection = collection_selector(item, index)
                # Run through the given collection, and return the item - with or without using the result selector
                for collection_item in collection:
                    if result_selector is None:
                        yield collection_item
                    else:
                        yield result_selector(item, collection_item)
        return Linq(GeneratorIterable(select_many_generator))

    #
    # Sorting Operators
    #

    def order_by(self, key_selector: typing.Callable=None) -> "Linq":
        """
        Implements the order by linq operator
        :param key_selector: A callable to obtain the key for each item to be used for comparison
        :return: A new Linq object which contains the original range ordered by the key
        """
        self._check_callable(key_selector, name="key_selector", optional=True)

        def order_by_generator():
            ordered = sorted(self._iterable, key=key_selector)
            for item in ordered:
                yield item
        return Linq(GeneratorIterable(order_by_generator))

    def order_by_descending(self, key_selector: typing.Callable=None) -> "Linq":
        """
        Implements the order by descending linq operator
        :param key_selector: A callable to obtain the key for each item to be used for comparison
        :return: A new Linq object which contains the original range ordered  descending by the key
        """
        self._check_callable(key_selector, name="key_selector", optional=True)

        def order_by_descending_generator():
            ordered = sorted(self._iterable, key=key_selector, reverse=True)
            for item in ordered:
                yield item
        return Linq(GeneratorIterable(order_by_descending_generator))

    def reverse(self) -> "Linq":
        """
        Implements the reverse linq operator
        :return: A new Linq object where the items are in reversed order
        """

        def reverse_generator():
            # We cannot use the built in reversed() directly on self._iterable
            # since it has requirements which are not fulfilled by generators
            # So first, we need to create a list out of self._iterable
            items = list(self._iterable)
            for item in reversed(items):
                yield item
        return Linq(GeneratorIterable(reverse_generator))

    #
    # Grouping Operators
    #

    def group_by(self, key_selector: typing.Callable,
                 element_selector: typing.Callable=None,
                 result_selector: typing.Callable=None) -> "Linq":
        """
        Implements the group ny linq operator
        :param key_selector: A callable to obtain the key for each item to be used for grouping
        :param element_selector: A callable to project each element in the groups
        :param result_selector: A callable to project groups (with keys and the items) to a final result
        :return: A new Linq object, containing the original items grouped by the key, provided by key_selector.
                 Optionally it projects the items in the groups with element_selector,
                 and projects the groups with result_selector
        """
        self._check_callable(key_selector, name="key_selector")
        self._check_callable(element_selector, name="element_selector", optional=True)
        self._check_callable(result_selector, name="result_selector", optional=True)

        def group_by_generator():
            groups = {}  # type: typing.Dict[typing.Any, typing.List[typing.Any]]
            # Group items according to the key_selector
            for item in self._iterable:
                key = key_selector(item)
                if key not in groups.keys():
                    groups[key] = []
                groups[key].append(item)
            # Project items if there is an element selector
            if element_selector:
                for key in groups:
                    items = groups[key]
                    del groups[key]
                    groups[key] = []
                    for item in items:
                        groups[key].append(element_selector(item))
            # Project the groups if there is a result selector
            if result_selector:
                for key in groups:
                    yield result_selector(key, groups[key])
            else:
                GroupByResult = collections.namedtuple("GroupByResult", ["key", "items"])
                for key in groups:
                    yield GroupByResult(key, groups[key])
        return Linq(GeneratorIterable(group_by_generator))

    #
    # Conversions Operators
    #

    def to_dictionary(self, key_selector: typing.Callable, result_selector: typing.Callable=None) -> typing.Dict:
        """
        Implements the to dictionary linq operator
        :param key_selector: The callable to retrieve the key for each item in the range
        :param result_selector: The optional callable, to retrieve the value from each item in tha range
                                to be stored as value in the resulting dictionary
        :return: A dictionary where the keys are the returned values from key_selector, and the values are either
                 the items themselves or the values returned by result_selector
        """
        self._check_callable(key_selector, name="key_selector")
        self._check_callable(result_selector, name="result_selector", optional=True)
        return_value = {}
        for item in self._iterable:
            key = key_selector(item)
            if result_selector is not None:
                item = result_selector(item)
            return_value[key] = item
        return return_value

    def to_list(self) -> typing.List:
        """
        Implements the to list linq operator
        :return: A list containing all the items from the range
        """
        return list(self._iterable)

    #
    # Concatenation Operators
    #

    def concat(self, iterable: typing.Iterable) -> "Linq":
        """
        Implements the concat linq operator
        :param iterable: The other iterable to concatenate the current Linq object with
        :return: A new Linq objects with items from the current range first and then the item
                 from the iterable parameter
        """
        self._check_iterable(iterable, name="iterable")

        def concat_generator():
            for item in self._iterable:
                yield item
            for item in iterable:
                yield item
        return Linq(GeneratorIterable(concat_generator))

    #
    # Aggregation Operators
    #

    def aggregate(self, accumulator: typing.Callable,
                  seed: typing.Any=None,
                  result_selector: typing.Callable=None) -> typing.Any:
        """
        Implements the aggregate linq operator
        :param accumulator: The callable used to calculate the result.
               The first argument is the seed, the second argument is the current item from the range
               If no seed provided, the seed will be the first item in the range
               It should return the new seed
        :param seed: The original value used for the seed
        :param result_selector: The final result will be transformed with this callable if provided
        :return: The aggregate result from the accumulator, possible transformed with the result_selector
        """
        self._check_callable(accumulator, name="accumulator")
        self._check_callable(result_selector, name="result_selector", optional=True)

        # Convert ourselves to a list
        items = list(self._iterable)
        # aggregate cannot work on empty ranges
        if not items:
            raise ValueError("Operator 'aggregate' cannot work on empty range")
        # Calculate initial seed - it is either the provided one, or the first item from the list
        if seed is None:
            seed = items[0]
            # If the first item is the seed, we do not need to use the first item anymore
            items = items[1:]
        # Calculate the result
        for item in items:
            seed = accumulator(seed, item)
        # Return the result with or without using the result_selector
        if result_selector:
            return result_selector(seed)
        return seed

    def average(self, selector: typing.Callable=None) -> typing.Any:
        """
        Implements the average linq operator
        :param selector: A callable that projects each item to another type to calculate the average on 
        :return: The average of the items in the range, or the average of the items provided by selector
        """
        self._check_callable(selector, name="selector", optional=True)
        count = 0
        total = 0
        for item in self._iterable:
            count += 1
            if selector:
                total += selector(item)
            else:
                total += item
        if count == 0:
            raise ValueError("Operator 'average' cannot work on empty range")
        return total / count

    def count(self, predicate: typing.Callable=None) -> int:
        """
        Implements the count linq operator
        :param predicate: If specified it is a callable to invoke for each element
                          to determine if t should be counted or not
        :return: The number of items in the range, which satisfy the predicate - if present.
                 If no predicate given, it returns the number of elements in the range
        """
        self._check_callable(predicate, name="predicate", optional=True)
        if predicate is None:
            items = []
            items.extend(self._iterable)
            return len(items)
        else:
            return self.where(predicate).count()

    def max(self, selector: typing.Callable=None) -> typing.Any:
        """
        Implements the max linq operator
        :param selector: A callable that projects each item to another type to calculate the max on
        :return: The biggest item in the range, or the biggest item provided by selector
        """
        self._check_callable(selector, name="selector", optional=True)
        items = list(self._iterable)
        if not items:
            raise ValueError("Operator 'max' cannot work on empty range")
        maximum = items[0]
        if selector:
            maximum = selector(maximum)
        items = items[1:]
        for item in items:
            if selector:
                item = selector(item)
            if item > maximum:
                maximum = item
        return maximum

    def min(self, selector: typing.Callable=None) -> typing.Any:
        """
        Implements the min linq operator
        :param selector: A callable that projects each item to another type to calculate the min on
        :return: The smallest item in the range, or the smallest item provided by selector
        """
        self._check_callable(selector, name="selector", optional=True)
        items = list(self._iterable)
        if not items:
            raise ValueError("Operator 'min' cannot work on empty range")
        minimum = items[0]
        if selector:
            minimum = selector(minimum)
        items = items[1:]
        for item in items:
            if selector:
                item = selector(item)
            if item < minimum:
                minimum = item
        return minimum

    def sum(self, selector: typing.Callable=None) -> int:
        """
        Implements the sum linq operator
        :param selector: A callable that projects each item to another type to calculate the sum on
        :return: The sum of item in the range, or the sum of items provided by selector
        """
        self._check_callable(selector, name="selector", optional=True)
        total = 0
        for item in self._iterable:
            if selector:
                total += selector(item)
            else:
                total += item
        return total

    #
    # Quantifier Operators
    #

    def all(self, predicate: typing.Callable) -> bool:
        """
        Implements the all linq operator
        :param predicate: The callable which checks if all item in the range fulfills a criteria 
        :return: True if all the items satisfy the predicate, False otherwise
        """
        self._check_callable(predicate, name="predicate")
        for item in self._iterable:
            if not predicate(item):
                return False
        return True

    def any(self, predicate: typing.Callable=None) -> bool:
        """
        Implements the any linq operator
        :param predicate: The callable which checks if any item in the range fulfills a criteria
        :return: True if any the item satisfies the predicate, False otherwise
                 Without a predicate, it returns True, if there is at least one item in the range, False otherwise
        """
        self._check_callable(predicate, name="predicate", optional=True)
        # If no predicate given, we just need to check if there is any item in the list
        if predicate is None:
            return bool(self._iterable)
        # Otherwise check if there is any item, satisfying the predicate
        for item in self._iterable:
            if predicate(item):
                return True
        return False

    def contains(self, value: typing.Any) -> bool:
        """
        Implements the contains linq operator
        :param value: The value to check if it is in the range
        :return: True if value found in the range, False otherwise
        """
        for item in self._iterable:
            if item == value:
                return True
        return False

    #
    # Partition Operators
    #

    def skip(self, count: int) -> "Linq":
        """
        Implements the skip linq operator
        :param count: The number of elements to skip from the original range
        :return: A new range which does not contain the first 'count' element
        """

        def skip_generator():
            skipped = 0
            for item in self._iterable:
                if skipped < count:
                    skipped += 1
                    continue
                yield item
        return Linq(GeneratorIterable(skip_generator))

    def skip_while(self, predicate: typing.Callable) -> "Linq":
        """
        Implements the skip while linq operator
        :param predicate: A callable to decide how many items to skip.
                          Items wil lbe skipped until predicate returns True
        :return: A new range, which will not contain the first items where the predicate returned true
        """
        self._check_callable(predicate, name="predicate")

        def skip_while_generator():
            skip = True
            for index, item in enumerate(self._iterable):
                if skip:
                    if predicate(item, index):
                        continue
                    else:
                        skip = False
                yield item
        return Linq(GeneratorIterable(skip_while_generator))

    def take(self, count: int) -> "Linq":
        """
        Implements the take linq operator
        :param count: The number of elements to take from the original range
        :return: A new range which contains only the first 'count' element
        """

        def take_generator():
            for index, item in enumerate(self._iterable):
                if index < count:
                    yield item
                    continue
                break
        return Linq(GeneratorIterable(take_generator))

    def take_while(self, predicate: typing.Callable) -> "Linq":
        """
        Implements the take while linq operator
        :param predicate: A callable to decide how many items to take.
                          Items wil lbe taken until predicate returns True
        :return: A new range, which will contain the first items where the predicate returned true
        """
        self._check_callable(predicate, name="predicate")

        def take_while_generator():
            for index, item in enumerate(self._iterable):
                if predicate(item, index):
                    yield item
                    continue
                break
        return Linq(GeneratorIterable(take_while_generator))

    #
    # Set Operators
    #

    def distinct(self) -> "Linq":
        """
        Implements the distinct linq operator
        :return: A new range object, where every item is only included once
        """

        def distinct_generator():
            for item in set(self._iterable):
                yield item
        return Linq(GeneratorIterable(distinct_generator))

    def exclude(self, iterable: typing.Iterable) -> "Linq":
        """
        Implements the except linq operator. The name has to be different, since "except" is a reserved word in Python
        :param iterable: The iterable with the elements to remove from the current range
        :return A new range object without the items in iterable
        """
        self._check_iterable(iterable, name="iterable")

        def exclude_generator():
            set_a = set(self._iterable)
            set_b = set(iterable)
            for item in set_a - set_b:
                yield item
        return Linq(GeneratorIterable(exclude_generator))

    def intersect(self, iterable: typing.Iterable) -> "Linq":
        """
        Implements the intersect linq operator
        :param iterable: The iterable with the elements to intersect with the current range
        :return: A new range object with the items present in both range and iterable
        """
        self._check_iterable(iterable, name="iterable")

        def intersect_generator():
            set_a = set(self._iterable)
            set_b = set(iterable)
            for item in set_a & set_b:
                yield item
        return Linq(GeneratorIterable(intersect_generator))

    def union(self, iterable):
        """
        Implements the union linq operator
        :param iterable: The iterable with the elements to unite with the current range
        :return: A new range with the items present in either range or iterable
        """
        self._check_iterable(iterable, name="iterable")

        def union_generator():
            set_a = set(self._iterable)
            set_b = set(iterable)
            for item in set_a | set_b:
                yield item
        return Linq(GeneratorIterable(union_generator))

    #
    # Equality Operators
    #

    def sequence_equal(self, iterable: typing.Iterable) -> bool:
        """
        Implements the sequence equal linq operator
        :param iterable: The other iterable to compare the range with
        :return: True, if the current range, and iterable contains the same items, False otherwise
        """
        self._check_iterable(iterable, name="iterable")
        count_a = self.count()
        count_b = Linq(iterable).count()
        if count_a != count_b:
            return False
        for item_a, item_b in zip(self._iterable, iterable):
            if item_a != item_b:
                return False
        return True

    #
    # Element Operators
    #

    def element_at(self, index: int) -> typing.Any:
        """
        Implements the element at linq operator
        :param index: The index of the wanted item
        :return: The item at the requested index. It throws an IndexError, if no such item was found
        """
        counter = 0
        for item in self._iterable:
            if counter == index:
                return item
            counter += 1
        raise IndexError()

    # Since iterable classes can hold any kind of item, we cannot be sure what type can be the default,
    # so the user must provide the default "fallback" value
    def element_at_or_default(self, index: int, default: typing.Any=None) -> typing.Any:
        """
        Implements the element at linq operator
        :param index: The index of the wanted item
        :param default: The default value to return with if no item found with the requested index
        :return: The item at the requested index or default if no such item was found
        """
        try:
            return self.element_at(index)
        except IndexError:
            return default

    def first(self, predicate: typing.Callable=None):
        """
        Implements the first linq operator
        :param predicate: A callable object capable of handling two positional arguments, item and index (in that order)
                          and returns a boolean
        :return: The first item satisfying the predicate, or if no predicate given, the first item from the range
                 If no such item found it raises an IndexError
        """
        if predicate is None:
            return self.element_at(0)
        else:
            return self.where(predicate).first()

    def first_or_default(self, predicate: typing.Callable=None, default: typing.Any=None) -> typing.Any:
        """
        Implements the first or default linq operator
        :param predicate: A callable object capable of handling two positional arguments, item and index (in that order)
                          and returns a boolean
        :param default: The default value to return with if no first item could be found
        :return: The first item satisfying the predicate, or if no predicate given, the first item from the range
                 If no such item found it returns the default parameter
        """
        self._check_callable(predicate, name="predicate", optional=True)
        try:
            return self.first(predicate)
        except IndexError:
            return default

    def last(self, predicate: typing.Callable=None) -> typing.Any:
        """
        Implements the last linq operator
        :param predicate: A callable object capable of handling two positional arguments, item and index (in that order)
                          and returns a boolean
        :return: The last item satisfying the predicate, or if no predicate given, the last item from the range
                 If no such item found it raises an IndexError
        """
        self._check_callable(predicate, name="predicate", optional=True)
        if predicate is None:
            count = self.count()
            return self.element_at(count - 1)
        else:
            return self.where(predicate).last()

    def last_or_default(self, predicate: typing.Callable=None, default: typing.Any=None) -> typing.Any:
        """
        Implements the last or default linq operator
        :param predicate: A callable object capable of handling two positional arguments, item and index (in that order)
                          and returns a boolean
        :param default: The default value to return with if no last item could be found
        :return: The last item satisfying the predicate, or if no predicate given, the last item from the range
                 If no such item found it returns the default parameter
        """
        self._check_callable(predicate, name="predicate", optional=True)
        try:
            return self.last(predicate)
        except IndexError:
            return default

    def single(self, predicate: typing.Callable=None) -> typing.Any:
        """
        Implements the single linq operator
        :param predicate: A callable object capable of handling two positional arguments, item and index (in that order)
                          and returns a boolean
        :return: The one and only item satisfying the predicate, or if no predicate given, the only item from the range
                 If there are no or more item it raises an IndexError
        """
        self._check_callable(predicate, name="predicate", optional=True)
        if self.count(predicate) != 1:
            raise IndexError()
        return self.first(predicate)

    def single_or_default(self, predicate: typing.Callable=None, default: typing.Any=None) -> typing.Any:
        """
        Implements the single or default linq operator
        :param predicate: A callable object capable of handling two positional arguments, item and index (in that order)
                          and returns a boolean
        :param default: The default value to return with if no item could be found, or more than one found
        :return: The one and only item satisfying the predicate, or if no predicate given, the only item from the range
                 If there are no or more items it returns the default parameter
        """
        self._check_callable(predicate, name="predicate", optional=True)
        try:
            return self.single(predicate)
        except IndexError:
            return default

    #
    # Private methods
    #

    @staticmethod
    def _check_iterable(iterable: typing.Iterable, name: str) -> None:
        """
        Helper method to check if an object is iterable. Throws TypeError if it is not
        :param iterable: The object to check
        :param name: The name of the iterable. Used for constructing the exception
        :return: None
        """
        try:
            # Iter will try to fetch the iterator, and raises a TypeError if something is not OK
            iter(iterable)
        except TypeError:
            raise TypeError("Parameter '{}' must be an 'iterable' object".format(name))

    @staticmethod
    def _check_callable(callable_object: typing.Callable, name: str, optional: bool=False) -> None:
        """
        Helper method to check if an object is callable. Throws TypeError if it is not
        :param callable_object: The object to check
        :param name: The name of the iterable. Used for constructing the exception
        :param optional: If true, callable_object can be None
        :return: 
        """
        if not callable(callable_object):
            # If the parameter is optional, it can be None, which is OK
            if optional and callable_object is None:
                return
            raise TypeError("Parameter '{}' must be a 'callable' object".format(name))

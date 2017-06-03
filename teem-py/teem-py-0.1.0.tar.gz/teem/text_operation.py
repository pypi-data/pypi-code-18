class Component():
    """Base functionality for an operation component."""

    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return '<{0.__class__.__name__:.1}{0.value!r}>'.format(self)

    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.value == other.value

    def size(self):
        raise NotImplementedError

    def shorten(self, size):
        raise NotImplementedError


class Retain(Component):
    """Operation component for retaining characters."""

    def size(self):
        return self.value

    def shorten(self, size):
        return Retain(self.value - size)


class Insert(Component):
    """Operation component for inserting characters."""

    def size(self):
        return len(self.value)

    def shorten(self, size):
        return Insert(self.value[size:])


class Delete(Component):
    """Operation component for deleting characters."""

    def size(self):
        return self.value

    def shorten(self, size):
        return Delete(self.value - size)


class TextOperation():
    """Diff between two strings."""

    def __init__(self, components=[]):
        self.components = list(components)

    def __repr__(self):
        return ''.join(repr(component) for component in self.components)

    def __eq__(self, other):
        return (
            isinstance(other, TextOperation) and
            self.components == other.components
        )

    def __add__(self, component):
        if isinstance(component, Retain):
            return self._add_retain(component)
        elif isinstance(component, Insert):
            return self._add_insert(component)
        elif isinstance(component, Delete):
            return self._add_delete(component)
        raise TextOperationError('Unknown operation component')

    def _add_retain(self, component):
        """Returns a new operation with an added retain component."""
        op = TextOperation(components=self.components)
        if component.size() == 0:
            # If the retain is 0-length, it's a noop, so ignore it
            return op
        elif op.components and isinstance(op.components[-1], Retain):
            # If the previous component is also a retain, combine them
            op.components[-1] = Retain(
                op.components[-1].size() + component.size())
        else:
            # In all other cases, simply append the retain
            op.components.append(component)
        return op

    def _add_insert(self, component):
        """Returns a new operation with an added insert component."""
        op = TextOperation(components=self.components)
        if component.size() == 0:
            # If the insert is 0-length, it's a noop, so ignore it
            return op
        elif op.components and isinstance(op.components[-1], Insert):
            # If the previous component is also an insert, combine them
            op.components[-1] = Insert(
                op.components[-1].value + component.value)
        elif op.components and isinstance(op.components[-1], Delete):
            # If the previous component is a delete, the Insert comes before it
            if len(op.components) > 1 and isinstance(
                    op.components[-2], Insert):
                # Combine the insert with the penultimate component
                op.components[-2] = Insert(
                    op.components[-2].value + component.value)
            else:
                # Position the insert prior to the delete
                op.components.append(op.components[-1])
                op.components[-2] = component
        else:
            # In all other cases, simply append the insert
            op.components.append(component)
        return op

    def _add_delete(self, component):
        """Returns a new operation with an added delete component."""
        op = TextOperation(components=self.components)
        if component.size() == 0:
            # If the delete is 0-length, it's a noop, so ignore it
            return op
        elif op.components and isinstance(op.components[-1], Delete):
            # If the previous component is also a delete, combine them
            op.components[-1] = Delete(
                op.components[-1].size() + component.size())
        else:
            # In all other cases, simply append the delete
            op.components.append(component)
        return op

    @staticmethod
    def _shorten_components(a, b):
        """Shorten two ops by the part that cancels the other out."""
        if a.size() == b.size():
            return None, None
        if a.size() > b.size():
            return a.shorten(b.size()), None
        if b.size() > a.size():
            return None, b.shorten(a.size())

    def compose(self, other):
        """
        Combine two consecutive operations into one with the same effect.

        a    b | retain           | insert           | delete
        -------+------------------+------------------+-----------------
        retain | retain the       | insert the       | delete the
               | shortest len     | full amount of b | shortest len
        -------+------------------+------------------+-----------------
        insert | insert the       | insert the       | cancels out
               | shortest len     | full amount of b |
        -------+------------------+------------------+-----------------
        delete | delete the       | delete the       | delete the
               | full amount of a | full amount of a | full amount of a
        """
        op = TextOperation()
        a_components = iter(self.components)
        b_components = iter(other.components)
        a = None
        b = None
        while True:
            # Grab the next components from a and b
            if a is None:
                a = next(a_components, None)
            if b is None:
                b = next(b_components, None)
            # If we have no more a and no more b components, we're done
            if a is None and b is None:
                break
            # If a is a delete, use that
            if isinstance(a, Delete):
                op += a
                a = None
                continue
            # If b is an insert, use that
            if isinstance(b, Insert):
                op += b
                b = None
                continue
            # If a or b has run out, the operations are different lengths
            if a is None or b is None:
                raise TextOperationError('Cannot compose operations of '
                    'different lengths')
            # Combine the components
            min_size = min(a.size(), b.size())
            if isinstance(a, Retain) and isinstance(b, Retain):
                op += Retain(min_size)
            elif isinstance(a, Insert) and isinstance(b, Retain):
                op += Insert(a.value[:min_size])
            elif isinstance(a, Retain) and isinstance(b, Delete):
                op += Delete(min_size)
            a, b = self._shorten_components(a, b)
        return op

    def transform(self, other):
        """
        Transform two operations a and b to a' and b'.

        These will work such that b' applied after a will achieve the same
        result as a' applied after b.

        a    b | retain             | insert             | delete
        -------+--------------------+--------------------+-------------------
        retain | a' retains min len | a' retains len b   | b' deletes min len
               | b' retains min len | b' inserts         |
        -------+--------------------+--------------------+-------------------
        insert | a' inserts         | a' inserts         | a' inserts
               | b' retains len a   | b' retains len a   | b' retains len a
        -------+--------------------+--------------------+-------------------
        delete | a' deletes min len | a' retains len b   | noop
               |                    | b' inserts         |
        """
        a_components = iter(self.components)
        b_components = iter(other.components)
        a_prime = TextOperation()
        b_prime = TextOperation()
        a = None
        b = None
        while True:
            if a is None:
                a = next(a_components, None)
            if b is None:
                b = next(b_components, None)
            # If we have no more a and no more b components, we're done
            if a is None and b is None:
                break
            # If a is an insert, use it for a' and retain in b'
            if isinstance(a, Insert):
                a_prime += Insert(a.value)
                b_prime += Retain(a.size())
                a = None
                continue
            # If b is an insert, use it for b' and retain in a'
            if isinstance(b, Insert):
                a_prime += Retain(b.size())
                b_prime += Insert(b.value)
                b = None
                continue
            # If a or b has run out, the operations are different lengths
            if a is None or b is None:
                raise TextOperationError('Cannot transform operations of '
                    'different lengths')
            # Transform the components together
            min_size = min(a.size(), b.size())
            if isinstance(a, Retain) and isinstance(b, Retain):
                a_prime += Retain(min_size)
                b_prime += Retain(min_size)
            elif isinstance(a, Delete) and isinstance(b, Retain):
                a_prime += Delete(min_size)
            elif isinstance(a, Retain) and isinstance(b, Delete):
                b_prime += Delete(min_size)
            a, b = self._shorten_components(a, b)
        return a_prime, b_prime

    def apply(self, document):
        """Apply this operation to a string, returning the resulting string."""
        cursor = 0
        chunks = []
        for component in self.components:
            if isinstance(component, Retain):
                chunks.append(document[cursor:cursor + component.size()])
                cursor += component.size()
            elif isinstance(component, Insert):
                chunks.append(component.value)
            elif isinstance(component, Delete):
                cursor += component.size()
            else:
                raise TextOperationError('Unknown operation component')
        if cursor != len(document):
            raise TextOperationError('Operation length doesn\'t match '
                'document length')
        return ''.join(chunks)


class TextOperationError(Exception):
    """Unable to perform the text operation."""
    pass

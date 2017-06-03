class MemoryBackend():
    """
    Simple in-memory backend.

    Not really suitable for production, but easy reference implementation for
    testing.
    """

    def __init__(self, operations=[]):
        self.operations = list(operations)

    def save_operation(self, state, operation):
        """Save an operation in the database."""
        self.operations.append((state, operation))

    def get_subsequent_operations(self, state):
        """Return operations since the state provided."""
        i = -1
        subsequent_operations = []
        while self.operations[i][0] != state:
            subsequent_operations.append(self.operations[i])
            i -= 1
        return reversed(subsequent_operations)

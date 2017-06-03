from teem import OperationPayload


class Server():
    """Receives operations from clients, transforms, and replies to clients."""

    def __init__(self, document, storage):
        self.document = document
        self.storage = storage

    def receive_operation(self, operation_payload):
        """
        Handles an incoming operation from a client.

        Receives the operation, transforms it against all subsequent
        operations, applies it to the current document, and returns the
        operation to send to all clients.
        """
        parent = operation_payload.parent
        operation = operation_payload.operation
        subsequent_operations = self.storage.get_subsequent(operation_payload)
        for subsequent_operation in subsequent_operations:
            operation, _ = operation.transform(subsequent_operation.operation)
            parent = subsequent_operation.parent
        self.document = operation.apply(self.document)
        operation_payload = OperationPayload(
            parent,
            operation_payload.uuid,
            operation,
        )
        self.backend.save_operation(operation_payload)
        return operation_payload

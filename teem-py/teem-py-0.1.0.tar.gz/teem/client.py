import hashlib
import json
import uuid

from teem import OperationPayload


class Client():
    """
    Communicates changes to and from the server.

    Transforms incoming operations from the server to apply them on the client
    version of the document. Buffers operations from the client side and keeps
    them updated and ready to send to the server.
    """

    def __init__(self, document):
        self.document = document
        self.awaiting_ack = None
        self.buffer = None

    def _get_hash(self):
        """Determine a unique identifier for the state of the document."""
        document_json = json.dumps(self.document, sort_keys=True)
        return hashlib.sha1(document_json).hexdigest()

    def _get_uuid(self):
        """Return a unique identifier for an operation."""
        return uuid.uuid4().hex

    def _send_operation(self, operation):
        """Sends the operation to the server."""
        OperationPayload(self._get_hash(), self._get_uuid(), operation)

    def apply_client(self, operation):
        """Handles client-side changes to the document."""
        if self.awaiting_ack:
            if self.buffer:
                self.buffer = self.buffer.compose(operation)
            else:
                self.buffer = operation
        else:
            self._send_operation(self.hash, uuid, operation)
            self.awaiting_ack = operation
        self.document = operation.apply(self.document)

    def apply_server(self, operation):
        pass

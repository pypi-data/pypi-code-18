import gzip
import hashlib
import os
import tarfile


class StreamMeta(object):
    """Make metadata for chunks of a stream.
    """
    def __init__(self, log_handle):
        """Initialise the class.

        :arg file log_handle: Open writable handle to a log file.
        """
        self._log_handle = log_handle
        self._chunk_size = 10737418240 # 10 GB

        self._hash_sum = hashlib.md5()
        self._len = 0
        self._index = 0
        self.info = []

        self._log_message()

    def _current_file(self):
        return 'chunk_{:04d}'.format(self._index)

    def _log_message(self):
        self._log_handle.write('Calculating checksum for chunk: {}\n'.format(
            self._current_file()))

    def write(self, data):
        """Update checksum and take care of chunking.

        :arg str data: Block of data to write.
        """
        self._len += len(data)
        if self._len >= self._chunk_size:
            overhang = len(data) - (self._len - self._chunk_size)
            self._hash_sum.update(data[:overhang])
            self.flush(self._chunk_size)
            self._hash_sum = hashlib.md5()
            self._hash_sum.update(data[overhang:])
            self._len -= self._chunk_size
            self._index += 1
            self._log_message()
        else:
            self._hash_sum.update(data)

    def flush(self, size=0):
        self.info.append({
            'filename': self._current_file(),
            'md5': self._hash_sum.hexdigest(),
            'size': size or self._len})


class Pipe(object):
    """Stream chunking pipe.
    """
    def __init__(self):
        """Initialise the class.
        """
        read_fd, write_fd = os.pipe()
        read_handle = os.fdopen(read_fd)
        write_handle = os.fdopen(write_fd, 'w')

        self._read = read_handle.read
        self.write = write_handle.write
        self.flush = write_handle.flush

        self.set_file('', 0)

    def read(self, size=-1):
        """Read {size} bytes from the pipe.

        :arg int size: Number of bytes to read.
        """
        send_size = min(self.len, size)
        self.len = max(0, self.len - size)

        return self._read(send_size)

    def set_file(self, name, size):
        """Set the name and size of the file.

        :arg str name: Name of the file.
        :arg int size: Size of the file.
        """
        self.name = name
        self.len = size


def tgz_stream(fileobj, path):
    """Stream a directory as a gzipped tar to a file object.

    :arg object fileobj: File object.
    :arg str path: Path to a directory.
    """
    gzip_stream = gzip.GzipFile(mode='w', fileobj=fileobj, mtime=0)
    tar_stream = tarfile.open(mode='w|', fileobj=gzip_stream)
    tar_stream.add(path, arcname='data')
    tar_stream.close()
    gzip_stream.close()

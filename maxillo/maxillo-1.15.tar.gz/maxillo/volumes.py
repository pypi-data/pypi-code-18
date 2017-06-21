import hashlib
import logging
import io
import os
import tarfile
import tempfile

import drophi.types

LOGGER = logging.getLogger(__name__)

async def generate_archive(content_map):
    """
    Generate the gzipped tarball that will be usd to populate a volume. The content_map
    should be a dict with keys that are the full path inside the volume to the file and 
    values that are either
    1) a string (which will be encoded to UTF-8 for writing to the file)
    2) a byte array
    3) an IO buffer that has a read(size=int) function that returns a bytearray. This will be read until it returns something falsey
    """
    buf = io.BytesIO()
    archive = tarfile.open(mode='w:gz', fileobj=buf)
    # iterate over the keys in sorted order so the tarfile is built deterministically
    # we need that for our MD5 hash to work out the same way every time
    md5 = hashlib.md5()
    for filepath in sorted(content_map.keys()):
        md5.update(filepath.encode('utf-8'))
        LOGGER.debug("Added %s, md5 is now %s", filepath, md5.hexdigest())
        content = content_map[filepath]
        if hasattr(content, 'read'):
            _handle_stream_content(archive, filepath, content, md5)
        else:
            _handle_static_content(archive, filepath, content, md5)
    archive.close()
    return buf, md5.hexdigest()

async def populate(client, volumename, archive):
    LOGGER.debug("Populating %s with files", volumename)
    container = drophi.types.Container('authentise/maxillo:latest')
    container.entrypoint = 'true'
    container.volumes = [
        drophi.types.Mount(source=volumename, target='/data', readonly=False),
    ]
    LOGGER.debug("Starting up a container to attach to %s to push data to it", volumename)
    await container.run(client)
    await client.container_archive_put(container.id, '/data', archive.getvalue(), no_overwrite_dir_non_dir=True)
    LOGGER.debug("Put data archive in the temp container for %s. Removing temp container %s", volumename, container.id)
    await client.container_rm(container.id, force=True)
    LOGGER.debug("Removed temp container used to create volume %s", volumename)

def _handle_stream_content(archive, fullpath, content, md5):
    with tempfile.TempFile() as tempbuffer:
        while True:
            chunk = content.read(4096)
            if not chunk:
                return
            content.write(chunk)
            md5.update(chunk)
        archive.add(tempbuffer.name, fullpath)

def _handle_static_content(archive, fullpath, content, md5):
    content = content.encode('utf-8') if isinstance(content, str) else content
    tarinfo = tarfile.TarInfo()
    tarinfo.name = fullpath
    tarinfo.size = len(content)
    buf = io.BytesIO(content)
    md5.update(content)
    LOGGER.debug("Adding static content at %s of %s, md5 is now %s", fullpath, content, md5.hexdigest())
    archive.addfile(tarinfo, buf)


import asyncio
import hashlib
import importlib
import importlib.util
import logging
import os

import drophi.client
import drophi.types

import maxillo.templates
import maxillo.volumes

LOGGER = logging.getLogger(__name__)

class LoadError(Exception):
    pass

def _setup_templates(path):
    templates_path = os.path.join(path, 'templates')
    if os.path.exists(templates_path):
        maxillo.templates.set_environment(templates_path)
        LOGGER.info("Using template directory %s for jinja templates")
    else:
        LOGGER.info("No templates found at %s, templates will be disabled", templates_path)

async def source(path):
    _setup_templates(path)
    initpath = os.path.join(path, '__init__.py')
    if not os.path.exists(initpath):
        LOGGER.error("The path '%s' does not exist - you'll need it to load anything", path)
        return
    basename = os.path.basename(path)
    if not basename:
        basename = os.path.basename(path[:-1])
    spec = importlib.util.spec_from_file_location(basename, initpath)
    if not (spec and spec.loader):
        LOGGER.error('Failed to load %s', path)
        return
    try:
        main = spec.loader.load_module()
    except Exception as e:
        LOGGER.exception("Failed to load your definition module: %s", e)
        raise
    LOGGER.debug("Loaded %s", initpath)
    if not hasattr(main, 'create_application'):
        LOGGER.error(
            "Unable to find root application creator in %s. You must define an module-scoped function "
            "named 'create_application' that takes no arguments and returns a maxillo.definitions.Application "
            "that defines the services in your application"
        , mainpath)
    client = drophi.client.Client()
    application = main.create_application()
    volume_updates, service_updates = await application.updates(client)
    if not (volume_updates or service_updates):
        LOGGER.info("No updates to apply")
    for group in [volume_updates, service_updates]:
        await asyncio.gather(*group)
    await client.close()

class Service(drophi.types.Service):
    async def update(self, client, current):
        if not self._needs_update(current):
            LOGGER.debug("No updates for %s", self.name)
            return
        await client.service_update(current.id, current.version, self.to_payload())

    def _needs_update(self, current):
        current_payload = current.to_payload()
        new_payload = self.to_payload()
        result = any([
            current_payload.get(prop) != new_payload.get(prop)
        for prop in ('EndpointSpec', 'TaskTemplate')])
        return result

class Endpoint(drophi.types.Endpoint):
    pass

class Port(drophi.types.Port):
    pass

class Volume(drophi.types.Volume):
    PROPERTIES = ('driver', 'labels', 'name', 'options', 'scope')
    def __init__(self, *args, content=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.content = content

    def has_updates(self, other):
        comparable_labels = {k: v for k, v in other.labels.items() if k != 'contentmd5'}
        return not all([
            self.labels == comparable_labels,
            self.driver == other.driver,
            self.options == other.options,
            self.scope == other.scope,
        ])

    async def update(self, client, current):
        archive, contenthash = await maxillo.volumes.generate_archive(self.content)
        if self.has_updates(current):
            LOGGER.info("Detected a configuration change for %s, rebuilding", self)
        else:
            if current.labels['contentmd5'] == contenthash:
                LOGGER.info("No updates needed for %s", self)
                return
            else:
                LOGGER.info("Detected a content change for %s (%s -> %s), rebuilding content", self, current.labels['contentmd5'], contenthash)
        await self.delete(client)
        await self._create(client, archive, contenthash)
        LOGGER.info("Done building %s", self)

    async def create(self, client):
        LOGGER.debug("Creating %s and populating with file content", self)
        archive, contenthash = await maxillo.volumes.generate_archive(self.content)
        await self._create(client, archive, contenthash)

    async def _create(self, client, archive, contenthash):
        self.labels['contentmd5'] = contenthash
        await super().create(client)
        await maxillo.volumes.populate(client, self.name, archive)

    def __eq__(self, other):
        if not super().__eq__(other):
            return False
        return self.labels.get('md5') == other.labels.get('md5')

class Mount(drophi.types.Mount):
    pass

def _get_by_name(collection, name):
    for c in collection:
        if c.name == name:
            return c

class Application():
    "Your entire application"
    def __init__(self, services, volumes):
        self.services = services
        self.volumes  = volumes

    async def updates(self, client):
        services = client.service_ls()
        volumes = client.volume_ls()
        LOGGER.debug("Listing services and volumes")
        services, volumes = await asyncio.gather(services, volumes)
        service_updates, volume_updates = await asyncio.gather(
            self._get_updates(client, services, self.services),
            self._get_updates(client, volumes, self.volumes),
        )
        return volume_updates, service_updates

    async def _get_updates(self, client, current, definitions):
        updates = []
        for d in definitions:
            match = _get_by_name(current, d.name)
            if not match:
                updates.append(d.create(client))
                LOGGER.debug("Adding coroutine to create %s", d)
            else:
                updates.append(d.update(client, match))
                LOGGER.debug("Adding coroutine to update %s", d)
        return updates

import logging

from .. import utils
from ..queue.base import Queue
from .base import Worker


logger = logging.getLogger(__name__)


class Supervisor(Worker):
    """
    config:
        children: int - count
        child: Mapping - config for child worker
    """
    async def init(self):
        self._children = []
        groups = self.config.get('groups')
        self.context.on_stop.append(self.stop, groups)
        await super().init()
        if self.config.get('input') is None:
            for i in range(self.config.children):
                self.add_child(i)
            await self._wait(lambda w: w.init())
            self._super = False
        else:
            self._subs['child_input'] = Queue({}, loop=self.loop)
            self._subs['child_output'] = Queue({}, loop=self.loop)
            self._super = True

    def _wait(self, lmbd):
        return self.context.wait_all([lmbd(w) for w in self._children])

    def get_child_config(self):
        template = self.config.child
        conf = type(template)(template)
        conf['autorun'] = False
        conf['persist'] = True
        return conf

    def add_child(self, suffix=None):
        conf = self.get_child_config()
        cls = utils.import_name(conf.cls)
        if suffix or 'name' not in conf:
            suffix = suffix or len(self._children)
            conf['name'] = '{}.{}'.format(self.name, suffix)
        instance = cls(conf, context=self.context, loop=self.loop)
        if self.input is not None:
            instance.input = self._subs['child_input']
            instance.output = self._subs['child_output']
        self._children.append(instance)
        return instance

    async def put(self, *args, **kwargs):
        await self.output.put(*args, **kwargs)

    async def run(self, value=None):
        if not self._super:
            return await self._wait(lambda w: w.start())

        child_out = self._subs['child_output']
        queue_output = self.output
        while len(child_out):
            out_item = await child_out.get()
            if queue_output is not None:
                await queue_output.put(out_item)

        child_in = self._subs['child_input']
        await child_in.put(value)

        any_free = sum(i._is_sleep for i in self._children)
        if not any_free and self.config.children > len(self._children):
            instance = self.add_child(len(self._children))
            await instance.init()
            await instance.start()

        return await child_out.get()

    async def stop(self, force=True):
        await self._wait(lambda w: w.stop(force=force))

    async def status(self):
        status = await super().status()
        status['children'] = []
        for w in self._children:
            status['children'].append(await w.status())
        return status

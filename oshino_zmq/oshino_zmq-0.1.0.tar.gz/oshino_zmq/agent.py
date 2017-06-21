import json

import zmq

from zmq.asyncio import Context

from oshino import Agent


class ZmqAgent(Agent):

    @property
    def bind(self):
        return self._data.get("bind", None)

    @property
    def connect(self):
        return self._data["connect"]

    def parse_logentry(self, json_obj):
        return {"metric": 1,
                "tags": "log",
                "attributes": json_obj}

    async def process(self, event_fn):
        logger = self.get_logger()

        msg = await self.socket.recv().decode("UTF-8")
        logger.trace("Received msg: '{0}'".format(msg))
        json_obj = json.loads(msg)
        log_obj = self.parse_logentry(json_obj)
        event_fn(service=self.prefix, **log_obj)

    def on_start(self):
        self.ctx = Context()
        self.socket = ctx.socket(zmq.PULL)
        if self.bind:
            self.socket.bind(self.bind)
        else:
            self.socket.connect(self.connect)

    def on_stop(self):
        self.socket.close()

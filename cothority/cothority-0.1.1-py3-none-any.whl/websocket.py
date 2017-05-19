#!/usr/bin/env python3

import asyncio
import websockets
import status_pb2

async def getStatus(url):
    async with websockets.connect(url+'/Status/Request') as websocket:

        request = status_pb2.Request()
        out = request.SerializeToString()
        await websocket.send(out)
        print("> {}".format(out))

        stat = await websocket.recv()
        status = status_pb2.Response()
        status.ParseFromString(stat)
        print("< {}".format(status))

async def getBlocks(url):
    async with websockets.connect(url+'/Status/Request') as websocket:

        request = status_pb2.Request()
        out = request.SerializeToString()
        await websocket.send(out)
        print("> {}".format(out))

        stat = await websocket.recv()
        status = status_pb2.Response()
        status.ParseFromString(stat)
        print("< {}".format(status))

asyncio.get_event_loop().run_until_complete(getStatus('ws://dedis.ch:7003'))
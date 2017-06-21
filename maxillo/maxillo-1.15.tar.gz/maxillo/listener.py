import asyncio
import argparse
import functools
import json
import logging
import pprint

import aiohttp
import maxillo.deployments
import maxillo.networking

LOGGER = logging.getLogger("listen")

SSE_DELIMITER = '\r\n\r\n'
def initialize(exit_event, session, host=None):
    "Create the listener connection and return the queue where received events go"
    queue = asyncio.Queue()

    listen_task = asyncio.ensure_future(listen(exit_event, session, queue, host))

    return queue, listen_task

async def listen(exit_event, session, event_queue, host=None):
    try:
        retry = 0
        while not exit_event.is_set():
            try:
                headers = maxillo.deployments.generate_auth_headers('')
            except FileNotFoundError:
                LOGGER.info("Cannot find license file, waiting for it to arrive")
                await asyncio.sleep(3.0)
                continue

            LOGGER.info("Starting event listener")
            try:
                await asyncio.sleep(min((retry * 0.1)**1.5, 30))
                host = host or maxillo.deployments.load_license().master
                url = '{}/stream/'.format(host)
                proxy = maxillo.networking.get_proxy()
                async with session.get(url, headers=headers, timeout=0, proxy=proxy) as response:
                    LOGGER.debug("Status: %s", response.status)
                    retry = 0
                    buf = ''
                    while not exit_event.is_set():
                        if response.closed:
                            LOGGER.warning('Response from master closed, re-opening')
                            break
                        chunk = (await response.content.read(4096))
                        chunk = chunk.decode('utf-8')
                        buf += chunk
                        message_end = buf.find(SSE_DELIMITER)
                        while message_end >= 0:
                            text = buf[:message_end]
                            buf = buf[message_end + len(SSE_DELIMITER):]
                            message_end = buf.find(SSE_DELIMITER)
                            if text.startswith(':'):
                                LOGGER.debug("Ignoring comment message '%s'", text)
                            elif text == 'data: New client connection to stream':
                                LOGGER.debug("Ignoring connection message")
                            else:
                                if not text.startswith('data: '):
                                    LOGGER.warning("No data prefix on message '%s'", text)
                                    continue
                                else:
                                    text = text[len('data: '):]
                                try:
                                    message = json.loads(text)
                                    await event_queue.put(message)
                                except json.decoder.JSONDecodeError:
                                    LOGGER.warning("Not sure what to do with '%s', it isn't JSON", text)
            except (aiohttp.client_exceptions.ClientPayloadError,
                    aiohttp.client_exceptions.ServerDisconnectedError) as e:
                LOGGER.error("Got exception %s. Reconnecting...", e)
            except aiohttp.client_exceptions.ClientConnectorError as e:
                LOGGER.error("Failed to connect: %s. Reconnecting...", e)
            retry += 1
    except asyncio.CancelledError:
        LOGGER.debug("Listen coroutine was cancelled")
    except Exception as e:
        LOGGER.exception("Unhandled exception in listen(): %s", e)
    finally:
        LOGGER.info("Exited listen()")

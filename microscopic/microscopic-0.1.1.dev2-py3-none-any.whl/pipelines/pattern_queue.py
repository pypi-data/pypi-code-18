from microscopic import queue


async def pipeline(read_transport, write_transport, processor, pattern_factory):
    queue_manager = queue.PatternQueueManager(processor)

    with pattern_factory() as pattern:

        while True:
            data = await read_transport.read_chunk()
            if not data:
                break

            for strip, match in pattern.feed(data):
                queue_manager.push(strip, match)

            async for data in queue_manager.pump():
                await write_transport.write_chunk(data)

        # done reading; drain the pattern context and wait for the remaining queue results
        queue_manager.push(*pattern.drain())
        async for data in queue_manager.pump(wait=True):
            await write_transport.write_chunk(data)

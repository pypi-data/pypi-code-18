

async def execute_simple(
        pipeline,
        read_transport_factory,
        write_transport_factory,
        processor_factory,
        **kwargs):

    async with read_transport_factory() as read_transport, \
            write_transport_factory() as write_transport, \
            processor_factory() as processor:

        await pipeline(read_transport, write_transport, processor, **kwargs)

import aiohttp


class RequestProcessor():
    def __init__(self, request_factory):
        self._session = aiohttp.ClientSession()

        self.request_factory = request_factory

    async def __aenter__(self):
        await self._session.__aenter__()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self._session.__aexit__(exc_type, exc_val, exc_tb)

    async def __call__(self, data: memoryview) -> bytes:
        result = await self.request_factory(self._session, data)
        return result


async def short_url_factory(session: aiohttp.ClientSession, data: memoryview) -> bytes:
    url = bytes(data).decode('utf-8')

    coro = session.post('https://ptpb.pw/u',
                        json={'content': url},
                        headers={
                            'Accept': 'application/json',
                            'Content-Type': 'application/json'
                        })

    async with coro as response:
        data = await response.json()

    return bytes(data['url'].encode('utf-8'))

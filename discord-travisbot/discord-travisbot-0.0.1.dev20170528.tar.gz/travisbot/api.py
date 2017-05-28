"""Discord REST API tools."""

from aiohttp import ClientSession

from .conf import URL


async def api(path, method="GET", token=None, **kwargs):
    """Return the JSON body of a call to Discord REST API."""
    defaults = {
        "headers": {
            "User-Agent": "TravisBot (https://github.com/greut/travisbot)"
        }
    }

    if token:
        defaults["headers"]["Authorization"] = f"Bot {token}"

    kwargs = dict(defaults, **kwargs)

    with ClientSession() as session:
        url = f"{URL}{path}"
        async with session.request(method, url, **kwargs) as response:
            if response.status == 200:
                return await response.json()
            elif response.status == 400:
                error = await response.json()
                assert False, f"{response.reason}: {error}"
            else:
                assert False, response.reason

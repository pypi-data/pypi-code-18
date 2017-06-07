# -*- coding: utf-8 -*-
import traceback

from aiohttp.web import HTTPException, Response

__all__ = (
    'json_response_middleware',
)

from .web import json_response


def json_error(reason, status=500):
    return json_response({'error': True, 'error_msg': reason, 'data': None}, status=status)


def json_success(data):
    return json_response({'error': False, 'error_msg': None, 'data': data})


async def json_response_middleware(app, handler):
    async def middleware_handler(request):
        try:
            data = await handler(request)
            return data if isinstance(data, Response) else json_success(data)
        except HTTPException as exc:
            return json_error(exc.reason, exc.status_code)
        except:
            return json_error(traceback.format_exc())

    return middleware_handler

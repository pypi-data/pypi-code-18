# Copyright 2017 John Reese
# Licensed under the MIT license

from typing import Any, Generator, Iterable, Union


class ProxyCursor:
    pass


class ProxyConnection:
    def __init__(
        self,
    ) -> None:
        pass

    async def cursor(self) -> ProxyCursor:
        raise NotImplementedError('Not yet available in aiosqlite')

    async def commit(self) -> None:
        raise NotImplementedError('Not yet available in aiosqlite')

    async def rollback(self) -> None:
        raise NotImplementedError('Not yet available in aiosqlite')

    async def close(self) -> None:
        raise NotImplementedError('Not yet available in aiosqlite')

    async def execute(
        self,
        sql: str,
        parameters: Iterable[Any] = None,
    ) -> ProxyCursor:
        raise NotImplementedError('Not yet available in aiosqlite')

    async def executemany(
        self,
        sql: str,
        parameters: Union[Iterable[Iterable[Any]], Generator[Any]] = None,
    ) -> ProxyCursor:
        raise NotImplementedError('Not yet available in aiosqlite')

    async def executescript(
        self,
        sql_script: str,
    ) -> ProxyCursor:
        raise NotImplementedError('Not yet available in aiosqlite')


async def connect(
    database: str,
    *,
    timeout: float = 5.0,
    cached_statements: int = 100,
    uri: bool = False,
) -> ProxyConnection:
    pass

import abc

import httpx
import asyncio

MAX_TRIES = 10


class ResultsObserver(abc.ABC):
    @abc.abstractmethod
    def observe(self, data: bytes) -> None: ...


async def do_reliable_request(url: str, observer: ResultsObserver) -> None:
    """
    Одна из главных проблем распределённых систем - это ненадёжность связи.

    Ваша задача заключается в том, чтобы таким образом исправить этот код, чтобы он
    умел переживать возвраты ошибок и таймауты со стороны сервера, гарантируя
    успешный запрос (в реальной жизни такая гарантия невозможна, но мы чуть упростим себе задачу).

    Все успешно полученные результаты должны регистрироваться с помощью обсёрвера.
    """

    async with httpx.AsyncClient() as client:
        # YOUR CODE GOES HERE
        # количество ретраев
        n_tries = 0

        data = None
        while (n_tries < MAX_TRIES) and (data is None):
            try:
                response = await client.get(url, timeout=10)
                response.raise_for_status()
                data = response.read()
            except httpx.HTTPStatusError:
                await asyncio.sleep(2**n_tries)
                n_tries += 1

        observer.observe(data)
        return
        #####################

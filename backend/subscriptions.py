# subscriptions.py
import asyncio
import strawberry
from typing import AsyncGenerator
from schema import FilmType

# Système de pub/sub simple
subscribers = []

@strawberry.type
class Subscription:

    @strawberry.subscription
    async def film_ajoute(self, info:strawberry.Info) -> AsyncGenerator[FilmType, None]:
        queue = asyncio.Queue()
        subscribers.append(queue)
        try:
            while True:
                film = await queue.get()
                yield film
        finally:
            subscribers.remove(queue)

async def publish_film(film):
    for queue in subscribers:
        await queue.put(film)

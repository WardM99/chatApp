"""Websockets"""
from asyncio import Queue as AsyncQueue, Lock
from collections import defaultdict
from typing import Optional
from queue import Queue

from fastapi import Depends, Request, Response, FastAPI
from humps import camelize

from src.app.logic.groups_logic import logic_get_group_by_id
from src.database.models import Group

class LiveEventParameters:
    """Construct a live enent data object"""

    def __init__(self, method: str, path_ids: dict):
        """Initialize"""
        self.method: str = method
        self.path_ids: dict = path_ids

    async def json(self) -> dict:
        """Generate json dict for live event"""
        return {
            'method': self.method,
            'pathIds': {camelize(k): v for k, v in self.path_ids.items()},
        }

class DataPublisher:
    """Event Bus"""

    def __init__(self):
        """Initialize"""
        self.queues: list[AsyncQueue] = []
        self.broadcast_lock: Lock = Lock()


    async def subscribe(self) -> AsyncQueue:
        """Subscribe to the event bus"""
        queue: AsyncQueue = AsyncQueue()
        self.queues.append(queue)
        return queue


    async def unsubscribe(self, queue: AsyncQueue) -> None:
        """Unsubscribe to the event bus"""
        self.queues.remove(queue)


    async def broadcast(self, live_event: LiveEventParameters) -> None:
        """Notify all subscribed listeners"""
        data: dict = await live_event.json()

        async with self.broadcast_lock:
            for queue in self.queues:
                await queue.put(data)

# Map containing a publisher for each group
_publisher_by_group: dict[Optional[int], DataPublisher] = defaultdict(DataPublisher)

async def get_publisher(group: Group = Depends(logic_get_group_by_id)):
    """Get a publisher for the given group"""
    return _publisher_by_group[group.group_id]


async def live(request: Request, publisher: DataPublisher = Depends(get_publisher)):
    """
    Add the publisher for the current group to the queue
    Indicates to the middleware the event might trigger a live data event
    """
    queue: Queue = request.state.websocket_publisher_queue
    queue.put_nowait(publisher)


def install_middleware(app: FastAPI):
    """Middleware for sending actions upon successful requests to live endpoints"""
    @app.middleware("http")
    async def live_middleware(request: Request, call_next) -> Response:
        queue: Queue[DataPublisher] = Queue()
        request.state.websocket_publisher_queue = queue

        response: Response = await call_next(request)

        if 200 <= response.status_code < 300 and not queue.empty():
            if (publisher := queue.get_nowait()) is not None:
                path_ids: dict = request.path_params.copy()
                #del path_ids['group_id']
                live_event: LiveEventParameters = LiveEventParameters(
                    request.method,
                    path_ids
                )
                await publisher.broadcast(live_event)

        return response

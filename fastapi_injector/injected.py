from fastapi import Depends
from starlette.requests import HTTPConnection
from taskiq import TaskiqDepends, Context
from typing import Any, TypeVar, Generic, Annotated

from fastapi_injector.attach import get_injector_instance, get_injector_instance_taskiq

BoundInterface = TypeVar("BoundInterface", bound=type)


def Injected(interface: Generic[BoundInterface]) -> BoundInterface:  # pylint: disable=invalid-name
    """
    Asks your injector instance for the specified type,
    allowing you to use it in the route.
    """

    async def inject_into_route(conn: HTTPConnection) -> BoundInterface:
        return get_injector_instance(conn.app).get(interface)

    return Depends(inject_into_route)


def SyncInjected(interface: Generic[BoundInterface]) -> BoundInterface:  # pylint: disable=invalid-name
    """
    Asks your injector instance for the specified type,
    allowing you to use it in the route. Intended for use
    with synchronous interfaces.
    """

    def inject_into_route(conn: HTTPConnection) -> BoundInterface:
        return get_injector_instance(conn.app).get(interface)

    return Depends(inject_into_route)


def InjectedTaskiq(interface: Generic[BoundInterface]) -> BoundInterface:  # pylint: disable=invalid-name
    """
    Asks your injector instance for the specified type,
    allowing you to use it in the task.
    """

    async def inject_into_task(context: Annotated[Context, TaskiqDepends()]) -> BoundInterface:
        return get_injector_instance_taskiq(context.state).get(interface)

    return TaskiqDepends(inject_into_task)


def SyncInjectedTaskiq(interface: Generic[BoundInterface]) -> BoundInterface:  # pylint: disable=invalid-name
    """
    Asks your injector instance for the specified type,
    allowing you to use it in the route. Intended for use
    with synchronous interfaces.
    """

    def inject_into_task(context: Annotated[Context, TaskiqDepends()]) -> BoundInterface:
        return get_injector_instance_taskiq(context.state).get(interface)

    return TaskiqDepends(inject_into_task)

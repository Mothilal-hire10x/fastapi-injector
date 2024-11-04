"""
A simple integration of alecthomas' injector into FastAPI.
Exposes a dependency wrapper to use in your routes.
"""

from fastapi_injector.attach import (
    attach_injector,
    attach_injector_taskiq,
    get_injector_instance,
    get_injector_instance_taskiq,
)
from fastapi_injector.exceptions import InjectorNotAttached
from fastapi_injector.injected import (
    Injected,
    InjectedTaskiq,
    SyncInjected,
    SyncInjectedTaskiq,
)
from fastapi_injector.request_scope import (
    InjectorMiddleware,
    RequestScope,
    RequestScopeFactory,
    RequestScopeOptions,
    request_scope,
)

__all__ = [
    "attach_injector",
    "attach_injector_taskiq",
    "get_injector_instance",
    "get_injector_instance_taskiq",
    "Injected",
    "SyncInjected",
    "InjectedTaskiq",
    "SyncInjectedTaskiq",
    "InjectorNotAttached",
    "request_scope",
    "RequestScopeOptions",
    "RequestScope",
    "RequestScopeFactory",
    "InjectorMiddleware",
]

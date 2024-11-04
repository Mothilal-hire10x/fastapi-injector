# FastAPI Injector

A powerful dependency injection integration for FastAPI and Taskiq applications, built on top of the Python [injector](https://github.com/alecthomas/injector) library.

## Features

- Seamless integration with FastAPI and Taskiq
- Support for both synchronous and asynchronous dependencies
- Request-scoped dependency management
- Clean separation of concerns through dependency injection
- Resource cleanup for context-managed dependencies
- Easy testing support with dependency overrides

## Installation

```bash
pip install git+https://github.com/10XScale-in/fastapi-injector.git
```

## Quick Start

### FastAPI Integration

```python
from fastapi import FastAPI, Body
from fastapi_injector import attach_injector, Injected
from injector import Injector
from typing import Annotated

# Define your interfaces and implementations
class UserRepository(abc.ABC):
    @abc.abstractmethod
    async def save_user(self, user: User) -> None:
        pass

class PostgresUserRepository(UserRepository):
    async def save_user(self, user: User) -> None:
        # Implementation details
        pass

# Create and configure your FastAPI application
app = FastAPI()
injector = Injector()
injector.binder.bind(UserRepository, to=PostgresUserRepository)
attach_injector(app, injector)

# Use injection in your routes
@app.post("/users")
async def create_user(
    data: Annotated[dict, Body()],
    repo: UserRepository = Injected(UserRepository)
):
    await repo.save_user(data)
    return {"status": "success"}
```

### Taskiq Integration

```python
from taskiq import TaskiqState, Context
from fastapi_injector import attach_injector_taskiq, InjectedTaskiq

# Initialize Taskiq broker and state
broker = TaskiqBroker()
state = TaskiqState()

# Configure injection
injector = Injector()
injector.binder.bind(UserRepository, to=PostgresUserRepository)
attach_injector_taskiq(state, injector)

# Use injection in your tasks
@broker.task
async def process_user(
    user_id: int,
    repo: UserRepository = InjectedTaskiq(UserRepository)
):
    # Task implementation
    pass
```

## Request Scope

Enable request-scoped dependencies for better resource management:

```python
from fastapi_injector import InjectorMiddleware, request_scope, RequestScopeOptions

# Configure request scope
options = RequestScopeOptions(enable_cleanup=True)
app.add_middleware(InjectorMiddleware, injector=injector)
attach_injector(app, injector, options)

# Bind with request scope
injector.binder.bind(DatabaseConnection, to=PostgresConnection, scope=request_scope)
```

## Synchronous Dependencies

Use `SyncInjected` for synchronous dependencies in FastAPI:

```python
from fastapi_injector import SyncInjected

@app.get("/sync-endpoint")
def get_data(service: SyncService = SyncInjected(SyncService)):
    return service.process()
```

Or `SyncInjectedTaskiq` for Taskiq:

```python
@broker.task
def sync_task(service: SyncService = SyncInjectedTaskiq(SyncService)):
    return service.process()
```

## Testing

Override dependencies in your tests:

```python
import pytest
from fastapi.testclient import TestClient

@pytest.fixture
def test_app():
    injector = Injector()
    injector.binder.bind(UserRepository, to=MockUserRepository)
    app = FastAPI()
    attach_injector(app, injector)
    return app

def test_create_user(test_app):
    client = TestClient(test_app)
    response = client.post("/users", json={"name": "Test User"})
    assert response.status_code == 200
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request. For major changes, please open an issue first to discuss what you would like to change.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the BSD License - see the LICENSE file for details.

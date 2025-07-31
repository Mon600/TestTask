import datetime
import random
import uuid
from typing import AsyncGenerator
from unittest.mock import AsyncMock

import pytest_asyncio
from fastapi import FastAPI
from httpx import AsyncClient, ASGITransport

from app.db.models import OperationType
from app.dependencies.dependencies import get_service
from app.service.service import OperationService
from main import app


async def operation_side_effect(wallet_id: uuid.UUID, amount: int, operation: OperationType):
    balance = 1000
    if operation == OperationType.deposit:
        return balance + amount
    elif operation == OperationType.withdraw:
        if amount > balance:
            return None
        return balance - amount
    else:
        raise TypeError("Invalid operation type.")


async def history_side_effect(wallet_id: uuid.UUID, limit: int, offset: int):
    return [
        {
            'id': uuid.uuid4(),
            'operation_type': random.choice(list(OperationType)).value,
            'time': datetime.datetime(
                day=random.randint(1, 28),
                month=random.randint(1, 7),
                year=2025,
                hour=random.randint(0, 23),
                minute=random.randint(0, 59)
            ),
            'account_id': wallet_id
        } for _ in range(limit)
    ]


@pytest_asyncio.fixture(scope='function', autouse=True)
async def mock_service() -> AsyncMock:
    service = AsyncMock(spec=OperationService)
    service.create_wallet.return_value = uuid.uuid4()
    service.operation.side_effect = operation_side_effect
    service.balance.return_value = 1000
    service.history.side_effect = history_side_effect
    return service


@pytest_asyncio.fixture(scope="function", autouse=True)
async def configured_app() -> FastAPI:
    return app


@pytest_asyncio.fixture(scope="function", autouse=True)
def override_dependencies(configured_app: FastAPI, mock_service: AsyncMock):
    configured_app.dependency_overrides[get_service] = lambda: mock_service
    yield
    configured_app.dependency_overrides = {}


@pytest_asyncio.fixture(scope="function")
async def async_client(configured_app: FastAPI) -> AsyncGenerator[AsyncClient, None]:
    BASE_URL = "http://test"
    async with AsyncClient(
            transport=ASGITransport(app=configured_app),
            base_url=BASE_URL
    ) as client:
        yield client

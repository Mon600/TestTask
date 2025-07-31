import uuid

import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_create_wallet(async_client: AsyncClient, mock_service):
    response = await async_client.post('/wallets/create', follow_redirects=True)
    response_json = response.json()
    assert response.status_code == 201
    assert response_json['wallet_id']
    mock_service.create_wallet.assert_called_once()


@pytest.mark.asyncio
async def test_deposit_operation(async_client: AsyncClient, mock_service):
    response = await async_client.post(
        f'/wallets/{uuid.uuid4()}/operation',
        json={
            "operation": "DEPOSIT",
            'amount': 1000
        }
    )
    response_json = response.json()
    assert response.status_code == 200
    assert response_json['current_balance'] == 2000
    mock_service.operation.assert_called_once()


@pytest.mark.asyncio
async def test_negative_deposit_operation(async_client: AsyncClient, mock_service):
    response = await async_client.post(
        f'/wallets/{uuid.uuid4()}/operation',
        json={
            "operation": "DEPOSI",
            'amount': 1000
        }
    )
    response_json = response.json()
    assert response.status_code == 422
    assert response_json['detail'][0]['msg'] == "Input should be 'DEPOSIT' or 'WITHDRAW'"
    mock_service.operation.assert_not_called()

@pytest.mark.asyncio
async def test_withdraw_operation(async_client: AsyncClient, mock_service):
    response = await async_client.post(
        f'/wallets/{uuid.uuid4()}/operation',
        json={
            "operation": "WITHDRAW",
            'amount': 500
        }
    )
    response_json = response.json()
    assert response.status_code == 200
    assert response_json['current_balance'] == 500
    mock_service.operation.assert_called_once()

@pytest.mark.asyncio
async def test_negative_withdraw_operation(async_client: AsyncClient, mock_service):
    response = await async_client.post(
        f'/wallets/{uuid.uuid4()}/operation',
        json={
            "operation": "WITHDRAW",
            'amount': 1500
        }
    )
    response_json = response.json()
    assert response.status_code == 409
    assert response_json['detail'] == 'There are insufficient funds in the account.'
    mock_service.operation.assert_called_once()


@pytest.mark.asyncio
async def test_get_balance(async_client: AsyncClient, mock_service):
    response = await async_client.get(f"/wallets/{uuid.uuid4()}/balance")
    assert response.status_code == 200
    assert response.json()['balance'] == 1000
    mock_service.balance.assert_called_once()


@pytest.mark.asyncio
async def test_get_history(async_client: AsyncClient, mock_service):
    response = await async_client.get(f"/wallets/{uuid.uuid4()}/history", params={"offset": 0, "limit": 10})
    assert response.status_code == 200
    assert len(response.json()) == 10
    mock_service.history.assert_called_once()


@pytest.mark.asyncio
async def test_negative_get_history(async_client: AsyncClient, mock_service):
    response = await async_client.get(f"/wallets/{uuid.uuid4()}/history", params={"offset": 0, "limit": 0})
    assert response.status_code == 422
    assert response.json()['detail'][0]['msg'] == "Input should be greater than or equal to 1"
    mock_service.history.assert_not_called()

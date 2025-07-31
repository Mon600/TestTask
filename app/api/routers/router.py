from uuid import UUID

from fastapi import APIRouter, HTTPException

from app.dependencies.dependencies import ServiceDep
from app.pyadntic.models import HistorySchema, ParamsDep, PaginationDep

router = APIRouter(prefix='/wallets')


@router.post('/create', status_code=201)
async def create_wallet(service: ServiceDep):
    wallet_id = await service.create_wallet()
    if wallet_id:
        return {'ok': True, 'msg': "Wallet was successfully created!", "wallet_id": wallet_id}
    else:
        raise HTTPException(status_code=500, detail='Somthing went wrong! Try again later')


@router.post('/{wallet_id}/operation', status_code=200)
async def operation(service: ServiceDep, wallet_id: UUID, params: ParamsDep):
    try:
        balance = await service.operation(wallet_id, params.amount, params.operation)
        if balance:

            return {"ok": True, "current_balance": balance}
        else:
            raise HTTPException(status_code=409, detail="There are insufficient funds in the account.")
    except TypeError:
        raise HTTPException(status_code=422, detail="Invalid operation type. Available types: DEPOSIT or WITHDRAW")


@router.get('/{wallet_id}/balance', status_code=200)
async def get_balance(service: ServiceDep, wallet_id: UUID):
    balance = await service.balance(wallet_id)
    if balance is None:
        raise HTTPException(status_code=404, detail=f"Account with id {wallet_id} not found")
    return {'ok': True, 'balance': balance}


@router.get('/{wallet_id}/history', status_code=200)
async def get_history(service: ServiceDep, wallet_id: UUID, pagination: PaginationDep) -> list[HistorySchema]:
    history = await service.history(wallet_id, pagination.limit, pagination.offset)
    if not history:
        raise HTTPException(status_code=404, detail=f"This wallet has not operations yet or not exist.")
    return history

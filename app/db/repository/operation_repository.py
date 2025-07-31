from uuid import UUID

from sqlalchemy import update, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models import BankAccount, OperationType, History


class OperationRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self):
        new_wallet = BankAccount()
        self.session.add(new_wallet)
        await self.session.commit()
        return new_wallet.id

    async def deposit(self, wallet_id: UUID, amount: int, operation: OperationType):
        stmt = (update(BankAccount)
                .where(BankAccount.id == wallet_id)
                .values(balance=BankAccount.balance + amount)
                .returning(BankAccount.balance))

        res = await self.session.execute(stmt)
        balance = res.scalars().one()

        new_history_record = History(
            operation_type=operation,
            account_id=wallet_id,
            amount=amount
        )
        self.session.add(new_history_record)

        await self.session.commit()
        return balance

    async def withdraw(self, wallet_id: UUID, amount: int, operation: OperationType):
        stmt = (update(BankAccount)
                .where(BankAccount.id == wallet_id, BankAccount.balance >= amount)
                .values(balance=BankAccount.balance - amount)
                .returning(BankAccount.balance))

        res = await self.session.execute(stmt)
        balance = res.scalars().one_or_none()

        new_history_record = History(
            operation_type=operation,
            account_id=wallet_id,
            amount=amount
        )
        self.session.add(new_history_record)

        await self.session.commit()
        return balance

    async def get_balance(self, wallet_id: UUID):
        stmt = select(BankAccount).where(BankAccount.id == wallet_id)
        res = await self.session.execute(stmt)
        balance = res.scalars().one_or_none()
        return balance


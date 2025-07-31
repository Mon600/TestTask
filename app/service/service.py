import logging
from uuid import UUID

from app.db.models import OperationType
from app.db.repository.repository import Repository

logger = logging.getLogger(__name__)

class OperationService:
    def __init__(self, repository: Repository):
        self.repository = repository

    async def create_wallet(self):
        try:
            wallet_id = await self.repository.create()
            return wallet_id
        except Exception as e:
            logger.error(e)
            return None

    async def operation(self, wallet_id: UUID, amount: int, operation: OperationType):
        try:
            if operation == OperationType.withdraw:
                balance = await self.repository.withdraw(wallet_id, amount, operation)
            elif operation == OperationType.deposit:
                balance = await self.repository.deposit(wallet_id, amount, operation)
            else:
                raise TypeError("Invalid operation type")
            return balance
        except Exception as e:
            logger.error(e)
            return None

    async def balance(self, wallet_id: UUID):
        try:
            balance = await self.repository.get_balance(wallet_id)
            return balance
        except Exception as e:
            logger.error(e)
            return None

    async def history(self, wallet_id: UUID, limit: int, offset: int):
        try:
            history = await self.repository.get_history(wallet_id, limit, offset)
            return history
        except Exception as e:
            logger.error(e)
            return None

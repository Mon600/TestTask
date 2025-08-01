import logging
from uuid import UUID

from app.db.models import OperationType
from app.db.repository.operation_repository import OperationRepository
from app.db.repository.history_repositoriy import HistoryRepository



class OperationService:
    def __init__(self, operation_repository: OperationRepository, history_repository: HistoryRepository):
        self.operation_repository = operation_repository
        self.history_repository = history_repository
        self.logger = logging.getLogger(__name__)

    async def create_wallet(self):
        try:
            wallet_id = await self.operation_repository.create()
            return wallet_id
        except Exception as e:
            self.logger.error(e)
            return None

    async def operation(self, wallet_id: UUID, amount: int, operation: OperationType):
        try:
            if operation == OperationType.withdraw:
                balance = await self.operation_repository.withdraw(wallet_id, amount, operation)
            elif operation == OperationType.deposit:
                balance = await self.operation_repository.deposit(wallet_id, amount, operation)
            else:
                raise TypeError("Invalid operation type")
            return balance
        except Exception as e:
            self.logger.error(e)
            return None

    async def balance(self, wallet_id: UUID):
        try:
            balance = await self.operation_repository.get_balance(wallet_id)
            return balance
        except Exception as e:
            self.logger.error(e)
            return None

    async def history(self, wallet_id: UUID, limit: int, offset: int):
        try:
            history = await self.history_repository.get_history(wallet_id, limit, offset)
            return history
        except Exception as e:
            self.logger.error(e)
            return None

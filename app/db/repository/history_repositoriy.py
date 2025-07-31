from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models import History


class HistoryRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_history(self, wallet_id: UUID, limit: int, offset: int):
        stmt = select(History).where(History.account_id == wallet_id).offset(offset).limit(limit)
        res = await self.session.execute(stmt)
        history = res.scalars().all()
        return history

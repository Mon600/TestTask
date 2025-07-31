from typing import AsyncGenerator, Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.repository.history_repositoriy import HistoryRepository
from app.db.repository.operation_repository import OperationRepository
from app.service.service import OperationService
from config import async_session


async def get_session() -> AsyncGenerator:
    async with async_session() as session:
        try:
            yield session
        except Exception as e:
            await session.rollback()
            raise e
        finally:
            await session.close()


SessionDep = Annotated[AsyncSession, Depends(get_session)]


async def get_operation_repository(session: SessionDep) -> OperationRepository:
    return OperationRepository(session)


OperationRepositoryDep = Annotated[OperationRepository, Depends(get_operation_repository)]



async def get_history_repository(session: SessionDep) -> HistoryRepository:
    return HistoryRepository(session)


HistoryRepositoryDep = Annotated[HistoryRepository, Depends(get_history_repository)]


async def get_service(operation_repository: OperationRepositoryDep,
                      history_repository: HistoryRepositoryDep) -> OperationService:
    return OperationService(operation_repository, history_repository)


ServiceDep = Annotated[OperationService, Depends(get_service)]

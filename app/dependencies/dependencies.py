from typing import AsyncGenerator, Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.repository.repository import Repository
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


async def get_repository(session: SessionDep) -> Repository:
    return Repository(session)


RepositoryDep = Annotated[Repository, Depends(get_repository)]


async def get_service(repository: RepositoryDep) -> OperationService:
    return OperationService(repository)


ServiceDep = Annotated[OperationService, Depends(get_service)]

import datetime
import enum
from typing import Annotated
from uuid import UUID as pyUUID, uuid4

from sqlalchemy import UUID, CheckConstraint, text, ForeignKey
from sqlalchemy.orm import Mapped
from sqlalchemy.testing.schema import mapped_column

from config import Base

pkUUID = Annotated[pyUUID, mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid4)]


class OperationType(enum.Enum):
    deposit = "DEPOSIT"
    withdraw = "WITHDRAW"


class BankAccount(Base):
    __tablename__ = 'accounts'

    id: Mapped[pkUUID]
    balance: Mapped[int] = mapped_column(default=0)

    __table_args__ = (CheckConstraint("balance >=0"),)


class History(Base):
    __tablename__ = 'history'

    id: Mapped[pkUUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    operation_type: Mapped[OperationType] = mapped_column(index=True)
    time: Mapped[datetime.datetime] = mapped_column(server_default=text("TIMEZONE( 'utc', now())"))
    amount: Mapped[int] = mapped_column()
    account_id: Mapped[pyUUID] = mapped_column(ForeignKey('accounts.id', ondelete='CASCADE'), index=True)

    __table_args__ = (CheckConstraint("amount > 0"),)

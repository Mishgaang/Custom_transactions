from uuid import UUID
from fastapi import Depends
from fastapi.requests import Request

from app.core.db.db import DB
from app.core.db.transaction import Transaction
from app.domains.item.use_case import ItemUseCase, TransactionItemUseCase


class DIContainer:
    @staticmethod
    def get_db(request: Request) -> DB:
        return request.app.state.db

    @staticmethod
    def get_transactions_obj(request: Request) -> Transaction:
        return request.app.state.transactions

    @staticmethod
    def _get_transaction_id(request: Request) -> UUID | None:
        return request.cookies.get("X-Transaction-id")

    @staticmethod
    def get_transaction(
        transaction_obj: dict = Depends(get_transactions_obj),
        transaction_id: UUID = Depends(_get_transaction_id),
    ) -> Transaction | None:
        if transaction := transaction_obj.get(transaction_id):
            return transaction
        return None

    @staticmethod
    def get_item_usecase(
        db: DB = Depends(get_db),
        transaction_id: UUID = Depends(_get_transaction_id),
        transaction: UUID = Depends(get_transaction),
    ) -> ItemUseCase | TransactionItemUseCase:
        if transaction_id and transaction:
            return TransactionItemUseCase(transaction)
        return ItemUseCase(db=db)

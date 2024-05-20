from typing import Any
from uuid import UUID

from .transaction import Transaction
from .incrementor import Incrementor


class DB:
    def __init__(self) -> None:
        self.__data = {}

    def get(self, id: int | None = None) -> dict | None:
        if id:
            return self.__data.get(id)
        return self.__data

    def create(self, create_obj) -> int:
        id = Incrementor.get_next_id()
        self.__data[id] = {"id": id, **create_obj}

        return id

    def delete(self, id) -> None:
        if not self.get(id):
            raise ValueError("Id is not definite")
        del self.__data[id]

    def begin(self, transaction_obj: dict) -> UUID:
        new_transaction = Transaction(db=self)

        transaction_obj[new_transaction.id] = new_transaction

        return new_transaction.id

    def commit(self, transaction: Transaction):
        self.__data = transaction.get_merge_states()
        del transaction

from app.core.db.db import DB
from app.core.db.transaction import Transaction


class ItemUseCase:
    def __init__(self, db: DB) -> None:
        self.db = db

    def fetch_items(self):
        return tuple(self.db.get().values())

    def create_item(self, obj):
        return self.db.create(obj)

    def delete_item(self, id: int):
        return self.db.delete(id)


class TransactionItemUseCase:
    def __init__(self, transaction: Transaction) -> None:
        self.transaction = transaction

    def fetch_items(self):
        return self.transaction.get()

    def create_item(self, obj):
        return self.transaction.create(obj)

    def delete_item(self, id: int):
        return self.transaction.delete(id)

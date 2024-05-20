from typing import Union
from uuid import uuid4

from .incrementor import Incrementor


class Transaction:
    def __init__(self, db, parent: Union["Transaction", None] = None) -> None:
        self.id = str(uuid4())
        self.__parent = parent
        self.__db = db
        self.__create_data = {}
        self.__delete_data = []

    def get(self):
        return tuple(self.get_merge_states().values())

    def create(self, obj) -> int:
        id = Incrementor.get_next_id()
        self.__create_data[id] = {"id": id, **obj}

        return id

    def delete(self, id: int) -> None:
        if not self._is_exist(id):
            raise ValueError("Id was not find")

        self.__delete_data.append(id)

    def _is_exist(self, id: int) -> bool:
        # Start find row from self if not jump to parent and check not delete row in transactions
        for transaction in self:
            if (
                id in tuple(transaction.__create_data.keys())
                and id not in transaction.__delete_data
            ):
                return True

            if id in transaction.__delete_data:
                return False

        # in id not in transactions look to db
        if id in tuple(self.__db.get().keys()):
            return True

        return False

    def get_merge_states(self) -> dict:
        db_items: dict = self.__db.get().copy()

        for transaction in self:
            db_items.update(transaction.__create_data)

            for id in transaction.__delete_data:
                del db_items[id]

        return db_items

    def __iter__(self):
        current = self
        yield current

        if current.__parent is not None:
            return current.__parent

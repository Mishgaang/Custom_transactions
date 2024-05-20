class Incrementor:
    __counter = 0
    __instance = None

    def __new__(cls):
        if not cls.__instance:
            cls.__instance = super().__new__()
        return cls.__instance

    @classmethod
    def get_next_id(cls):
        cls.__counter += 1
        return cls.__counter

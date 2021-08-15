from ..baseprocess import BaseProcess


class BaseEmployee:
    pass


class BaseEmployee(BaseProcess):
    def __lt__(self, other: BaseEmployee):
        return self.queue.qsize() < other.queue.qsize()

    def __gt__(self, other: BaseEmployee):
        return self.queue.qsize() > other.queue.qsize()


class AnyEmployee(BaseEmployee):
    def __init__(self) -> None:
        raise NotImplementedError(
            "Employee isn't defined. Look at me, poor manager, I cannot employ anybody :c"
        )

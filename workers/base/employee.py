from .baseprocess import BaseProcess


class BaseEmployee(BaseProcess):
    name = "Employee"


class AnyEmployee(BaseEmployee):
    def __init__(self) -> None:
        raise NotImplementedError(
            "Employee isn't defined. Look at me, poor manager, I cannot employ anybody :c"
        )

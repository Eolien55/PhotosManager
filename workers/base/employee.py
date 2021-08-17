from .baseprocess import BaseProcess


class BaseEmployee(BaseProcess):
    name = "Employee"
    has_parent = True

    def __init__(self, *args, **kwgs):
        self.parent = args[0]
        super().__init__(*args[1:], **kwgs)


class AnyEmployee(BaseEmployee):
    def __init__(self) -> None:
        raise NotImplementedError(
            "Employee isn't defined. Look at me, poor manager, I cannot employ anybody :c"
        )

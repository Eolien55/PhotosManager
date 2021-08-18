from .baseprocess import Base

BaseProcess = Base["Process"]


class BaseEmployee(BaseProcess):
    name = "Employee"
    has_parent = True

    def __init__(self, *args, **kwgs):
        self.process_id = args[0]
        args = args[1:]
        super().__init__(*args, **kwgs)


class AnyEmployee(BaseEmployee):
    def __init__(self) -> None:
        raise NotImplementedError(
            "Employee isn't defined. Look at me, poor manager, I cannot employ anybody :c"
        )

from .baseprocess import Base

BaseProcess = Base["Process"]


class BaseSecretary(BaseProcess):
    name = "BaseSecretary"
    has_parent = True

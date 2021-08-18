from .baseprocess import Base

BaseThread = Base["Thread"]


class BaseSecretary(BaseThread):
    name = "BaseSecretary"
    has_parent = True

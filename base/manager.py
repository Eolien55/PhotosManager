from ..baseprocess import BaseProcess
from employee import AnyEmployee
from multiprocessing import Process

PROCESS_NUMBER = 20


class BaseManager(BaseProcess):
    target = AnyEmployee

    def __init__(self, *args, **kwgs):
        super().__init__(*args, **kwgs)
        self.employees = list[Process]

        for _ in range(PROCESS_NUMBER):
            self.employees.append(self.target(**kwgs))

    def start_childs(self):
        for process in self.employees:
            process.start()

    def less_used(self):
        return min(map(lambda x: x.queue.qsize(), self.employees))

    def send_all(self, msg):
        for employee in self.employees:
            employee.send(msg)

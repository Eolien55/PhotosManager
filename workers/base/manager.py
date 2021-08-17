from .baseprocess import BaseProcess
from .employee import AnyEmployee
from multiprocessing import Queue

EMPLOYEE_NUMBER = 2


class BaseManager(BaseProcess):
    name = "Manager"
    target = AnyEmployee
    target_args = 0

    def __init__(self, *args, **kwgs):
        target_args = args[: self.target_args]
        args = args[self.target_args :]

        super().__init__(*args, **kwgs)
        employees = list()

        counter = 0
        for _ in range(EMPLOYEE_NUMBER):
            if self.target.has_parent:
                employees.append(self.target(*target_args, counter, self, **kwgs))
            else:
                employees.append(self.target(*target_args, counter, **kwgs))
            counter += 1

        self.employees = employees

    def start_employees(self):
        """Start every employee"""
        for employee in self.employees:
            if employee._popen is None:
                employee.start()

    def before_start(self):
        self.start_employees()

    def least_used(self):
        """Find employee with the smallest queue and give him the job"""
        return min(self.employees)

    def send_all(self, msg):
        """Send message to every employee"""
        for employee in self.employees:
            employee.send(msg)

    def after_loop(self):
        # Sending all employees message to stop their job
        self.send_all("END")

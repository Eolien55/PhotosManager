from .baseprocess import Base
from .employee import AnyEmployee

EMPLOYEE_NUMBER = 2

BaseProcess = Base["Process"]


class BaseManager(BaseProcess):
    name = "Manager"
    target = AnyEmployee
    target_args = 0
    secretary_args = 0
    secretary = None

    def __init__(self, *args, **kwgs):
        target_args = args[: self.target_args]
        _args = args[self.target_args :]

        super().__init__(*_args, **kwgs)
        employees = list()

        if self.target.has_parent:
            for _ in range(EMPLOYEE_NUMBER):
                employees.append(self.target(*target_args, _, self, **kwgs))
        else:
            for _ in range(EMPLOYEE_NUMBER):
                employees.append(self.target(*target_args, _, **kwgs))

        self.employees = employees
        if self.muted:
            for employee in self.employees:
                employee.muted = True

        if self.secretary:
            secretary_args = args[: self.target_args + self.secretary_args]
            if self.secretary.has_parent:
                self.secretary = self.secretary(*secretary_args, self, **kwgs)
            else:
                self.secretary = self.secretary(*secretary_args, **kwgs)

    def start_employees(self):
        """Start every employee"""
        for employee in self.employees:
            if employee._popen is None:
                employee.start()
        

    def before_start(self):
        self.start_employees()
        if self.secretary:
            self.secretary.start()

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

        if self.secretary:
            self.secretary.send("END")

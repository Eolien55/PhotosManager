from .baseprocess import BaseProcess
from .employee import AnyEmployee
from multiprocessing import Queue

EMPLOYEE_NUMBER = 2


class BaseManager(BaseProcess):
    name = "Manager"
    target = AnyEmployee
    target_args = 0
    process_id = False
    handler_target = None
    responses = False

    def __init__(self, *args, **kwgs):
        target_args = args[: self.target_args]
        args = args[self.target_args :]

        if self.responses:
            self.low_queue = Queue()
            target_args = [self.low_queue] + target_args
            self.run = self._run
        super().__init__(*args, **kwgs)
        employees = list()

        if self.process_id:
            counter = 0
            for _ in range(EMPLOYEE_NUMBER):
                employees.append(self.target(counter, *target_args, **kwgs))
                counter += 1
        else:
            for _ in range(EMPLOYEE_NUMBER):
                employees.append(self.target(*target_args, **kwgs))

        self.employees = employees

        if getattr(self, "handler_target", None):
            self.handler = self.handler_target

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

    def _run(self):
        if hasattr(self, "before_loop"):
            self.before_loop()

        while True:
            try:
                msg = self.queue.get_nowait()
                event, args = msg
                if event == "END":
                    break
                del event, args

                self.dispatch(message)
            except Exception:
                pass

            try:
                msg = self.low_queue.get_nowait()
                event, args = msg
                if event == "END":
                    break
                del event, args

                self.dispatch(message)
            except Exception:
                pass

        if hasattr(self, "after_loop"):
            self.after_loop()

class TaskException(Exception):
    def __init__(self, message: str) -> None:
        super().__init__(message)
        self.message = message


class TaskNotFound(TaskException):
    ...


class InsertTaskException(TaskException):
    pass


class GetTaskException(TaskException):
    pass


class UpdateTaskException(TaskException):
    ...


class RemoveTaskException(TaskException):
    ...


class TaskNotFoundException(TaskException):
    ...

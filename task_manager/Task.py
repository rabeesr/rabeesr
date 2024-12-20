import time
class Task:
    """Representation of a task

    Attributes:
                - created - date
                - completed - date
                - name - string
                - unique id - number
                - priority - int value of 1, 2, or 3; 1 is default
                - due date - date, this is optional
    """
    def __init__(self, name : str, id: int, priority = 1, due_date = ''):
        """Initializing a task object"""
        self.name = name
        self.created = time.localtime()
        self.id = id
        self.status = 'Active'
        self.priority = priority
        self.completed = None
        self.due_date = due_date
        self.updated = time.localtime()
        # calculate the age which will always be 0 when a task is first created
        self.age = str(round((time.mktime(time.localtime()) - time.mktime(self.created))/86400)) + 'd'
    # A helper function which will update the age anytime a tasks class is initialized
    def update_age(self):
        self.age = str(round((time.mktime(time.localtime()) - time.mktime(self.created))/86400)) + 'd'

    # a string representation of a task
    def __str__(self):
        return f"The task name '{self.name}' (Priority: {self.priority}) with unique id {self.id}" \
        f'\nhas a status of {self.status} and was created' \
        f' on {time.asctime(self.created)}' \
        f' and last updated {time.asctime(self.updated)}'

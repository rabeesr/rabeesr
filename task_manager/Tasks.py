import Task as tk
import time
import pickle
from datetime import datetime
import re

class Tasks:
    """A list of `Task` objects."""
    # This is a helper function to find the maximum id in the list of tasks. This is used to create and store a unique id everytime the add function is called. 
    def find_max_id(self,list_of_tasks):
        """Helper function to find the maximum id in a list of tasks"""
        # initially set max_id to 1 because it will never be 1 so this is a good base condition
        max_id = -1
        # if the list of tasks is empty, then set the max_id to 0
        if list_of_tasks == []:
            max_id = 0
        else:
        # cycle through each task in the list of tasks and find the maximum id by comparing the task id to the currently stored maximum id. 
        # If the task id is greater than the currently stored maximum id, then store it as the new maximum id.
            for task in list_of_tasks:
                if task[0].id > max_id:
                    max_id = task[0].id
        #finally return the max_id as the output of the function.
        return max_id
    
    def __init__(self):
        """Read pickled tasks file into a list"""
        # Try to open the .todo.pickle file
        try:
            f2 = open('./.todo.pickle', 'rb')
        except:
            # if the file can't be opened, then it doesn't exist and therefore we will create a new empty pickle file and store an empty list of tasks.
            f2 = open('./.todo.pickle', 'wb')
            self.tasks = list()
            self.list_of_task_ids = list()
            pickle.dump(self.tasks,f2)
            f2.close()
            # set the max_id to 0 if the list is empty. I understand this is redundant and can likely be removed because the max_id will be calculated from the helper function anyways.
            self.max_id = 0
        else:
            # if there is no exception raised, then load the pickle file into the list of task objects.
            self.tasks = pickle.load(f2)
            # find maximum id in the list of objects and store it
            self.max_id = self.find_max_id(self.tasks)
            # create an empty list of task_ids, these list of task_ids will be passed into the report function to report on a list of ALL tasks.
            self.list_of_task_ids = list()
            # sort the list of tasks by due_date and then priority. Tasks with priority 3 are the highest priority and tasks with priority 1 are the lowest priority.
            self.tasks.sort(key = lambda x: x[0].priority, reverse = True)
            self.tasks.sort(key=lambda x: x[0].due_date)
            # go through each task in the list of tasks and perform two operations. One operation is to update the age by calling the update_age function. 
            # The second operation is to append the task_ids to the list_of_task_ids to report on later.
            for task in self.tasks:
                task[0].update_age()
                self.list_of_task_ids.append(task[0].id)
            f2.close()
    # helper function which is called after add, delete, and complete operations to pickle the list of tasks.
    def pickle_tasks(self):
        """Picle your task list to a file"""
        f2 = open('./.todo.pickle', 'wb')
        pickle.dump(self.tasks,f2)
        f2.close()
    # This helper function is used to find the task for which to perform a completion, deletion, or update on.
    def find_task(self,task_id):
        """Helper function to return the index of the task based on a task_id. """
        index = [task[1] for task in self.tasks].index(task_id)
        return index
    
    def delete_task(self,task_id):
        """Function to delete tasks based on the task_id"""
        # Try to find the task_id in the list of tasks. If it exists then continue to the else portion of the code. 
        # If it doesn't exist print a message to the user informing them that the task id could not be found.
        try:
            delete_task_index = self.find_task(task_id)
            delete_task_index2 = self.list_of_task_ids.index(task_id)
        except:
            print('This task id does not exist')
        else:
            # If the task_id exists in the list of tasks then delete it from the list_of_task_ids and the collection of task objects
            del self.list_of_task_ids[delete_task_index2]
            del self.tasks[delete_task_index]
            # print a message to the user confirming that the task was deleted.
            print(f'Task {task_id} was successfully deleted')
            # Pickle the updated list of task objects.
            self.pickle_tasks()

    def list(self):
        # For the list method, filter out any completed/done tasks from the list of task objects.
        list_of_non_completed_tasks = filter(lambda x: x[0].status != 'Done', self.tasks)
        list_of_task_ids = []
        # Iterate through the list of task objects that are not in a "Done" status 
        # and store the task_ids in a list so that it can be passed to the report function.
        for task in list_of_non_completed_tasks:
            list_of_task_ids.append(task[0].id)
        #call the report function.
        self.report(list_of_task_ids)

    def report(self,list_of_task_ids):
        """A general report function which is utilized to report/print important Task information to the user based on a list of provided task ids
        This function is generalized so that the same reporting format is applied to queries, the list function, and a general report where all tasks are printed"""
        # Create and store a list of tasks that need to be reported on.
        list_of_tasks_to_report = []
        # Print the header columns to the user
        print(f"{'ID': <5}{'Age ': <5}{'Due Date': <12}{'Priority':<10}{'Task':<25}{'Created':<30}{'Completed':<30}")
        print(f"{'--':<5}{'---':<5}{'----------':<12}{'--------':<10}{'-------------------':<25}{'------------------------':<30}{'------------------------':<30}")
        # Iterate through the task_ids that are in the argument provided to the function and store the task in the list of tasks to report on.
        for task in list_of_task_ids:
            index = self.find_task(task)
            list_of_tasks_to_report.append(self.tasks[index][0])
        # Sort the tasks to report on by priority and due date. Tasks with upcoming due_dates (if one exists) are printed first. 
        # If two tasks have the same due date, then sort by descending priority where Priority 3 tasks are highest priority. 
        # A lambda function is passed into the key in the sort function to sort by the appropriate task attribute.
        list_of_tasks_to_report.sort(key = lambda x: x.priority, reverse = True)
        list_of_tasks_to_report.sort(key=lambda x: x.due_date)
        # Now that the list of tasks to report are sorted based on the above criteria, iterate through each task and print the corresponding information/attribute.
        for task in list_of_tasks_to_report:    
            # convert the created date into a user friendly string
            created_date = time.asctime(task.created)
            # If the completed date is not blank, then convert the completion date into a user friendly string, else print '-'
            if task.completed is not None:
                completed_date = time.asctime(task.completed)
            else:
                completed_date = '-'
            # If the due date year is not 9999, then print the due date in the appropriate format, else print '-'
            if task.due_date.year != 9999:
                # format the due date into a readable string in month/day/year format, 
                # if the duedate has the year 9999 then it was not provided and 9999 is used as a placeholder so that sort places it at the bottom (i.e. due date in very far future)
                due_date = task.due_date.strftime("%m/%d/%Y")
            else:
                #
                due_date = '-'
            print(f'{task.id:<5}{task.age: <5}{due_date:<12}{task.priority:<10}{task.name:<25}{created_date:<30}{completed_date:<30}')

    def done(self, id):
        """This function is utilized to complete tasks based on a provided task id"""
        # Try to find the task id in the list of task objects. If it exists, continue to the else portion of the code
        # Return a message to the user if it doesn't exist
        try:
            task_index = self.find_task(id)
        except:
            print('This task id does not exist')
        else:
            # If the task id exists, then change the status of the task to Done and store the task completion date as the current date in which it was completed.
            self.tasks[task_index][0].status = 'Done'
            self.tasks[task_index][0].completed = time.localtime()
            # pickle the updated list of task objects
            self.pickle_tasks()
            # print a message to the user informing them that the task was successfully completed.
            print(f'Completed Task {self.tasks[task_index][0].id}')

    def query(self, set_of_keywords):
        """This function is utilized to filter the list of task objects based on a set of keywords that are passed in"""
        # initialize an empty set of keywords
        list_of_indexes_keyword_match = set()
        # For each keyword in the set, check the task name to see if it contains the keyword in it.
        for keyword in set_of_keywords:
            for task in self.tasks:
                # compare the lowercase version of each keyword and task name since it is a non-case sensitive query
                if keyword.lower() in task[0].name.lower():
                    # if the task name contains the keyword, then add it to the set of unique tasks which contain the keyword(s)
                    list_of_indexes_keyword_match.add(task[0].id)
        # call the report function to report and print the list of matched keywords to the user. 
        # If no tasks are found then a blank list is reported to the user.
        self.report(list_of_indexes_keyword_match)
                    
    def add(self, task_name, priority = 1, due_date = ''):
        """This function is utilized to add a task object to the list of tasks in the Tasks class."""
        try:
            # This is the regex pattern used for validating the format of due date is in Month/Day/Year
            date_string = r'^(0?[1-9]|1[0-2])/(0?[1-9]|[12][0-9]|3[01])/(19|20)\d{2}$'
            # Check to ensure that a priority of either 1, 2, 3 is passed in by the user. If it is not, then return a message to the user. 
            # By default, if a priority is not provided, create a task with a low priority (i.e. priority of 1)
            if priority not in (1,2,3):
                print(f'Sorry this task could not be added. Please pick a priority between 1 and 3, with 3 being the highest priority')
            # Check to see if a due date is provided, if one is provided then make sure it matches the Month/Day/Year format. 
            # If the format is good, then continue by creating the task with the provided due date and priority. If it is not in the right format, return a message to the user.
            elif due_date is not None:
                if not(re.match(date_string, due_date)):
                    print(f'Sorry this task could not be added. Please add a due date in the format Month/Day/Year')
                else:
                    due_date = datetime.strptime(due_date, '%m/%d/%Y')
                    task = tk.Task(task_name, self.max_id + 1, priority, due_date)
                    self.tasks.append((task, task.id))
                    print(f'Created task {task.id}')
                    # update the max_id stored in the Tasks class object so that the next task id that is created is unique and incremented by 1.
                    self.max_id += 1
                    # Resort the updated list of tasks by due date and priority. 
                    # If two tasks have the same due date, then sort by descending priority where Priority 3 tasks are highest priority. 
                    # A lambda function is passed into the key in the sort function to sort by the appropriate task attribute.
                    self.tasks.sort(key = lambda x: x[0].priority, reverse = True)
                    self.tasks.sort(key=lambda x: x[0].due_date)
                    # pickle the updated list of task objects.
                    self.pickle_tasks()
            # if the due date is None, then store it as an empty string so that the sort function when reporting still works.
            elif due_date is None:
                    # create a dummy date very far into the future in year 9999 so that sort places the tasks without a due date at the bottom
                    due_date = datetime.strptime('12/31/9999', '%m/%d/%Y')
                    task = tk.Task(task_name, self.max_id + 1, priority, due_date)
                    self.tasks.append((task, task.id))
                    print(f'Created task {task.id}')
                    self.max_id += 1
                    # Resort the updated list of tasks by due date and priority. 
                    # If two tasks have the same due date, then sort by descending priority where Priority 3 tasks are highest priority. 
                    # A lambda function is passed into the key in the sort function to sort by the appropriate task attribute.
                    self.tasks.sort(key = lambda x: x[0].priority, reverse = True)
                    self.tasks.sort(key=lambda x: x[0].due_date)
                    self.pickle_tasks()
        # raise a value error for any general errors that occur when creating a task and appending it to the list of task objects.
        except ValueError:
            print('Sorry there was an error adding the task. Please make sure all the data is in the appropriate format.')
    # Overwrite the built in string function so that printing a tasks object returns a message informing the user with the number of tasks in the collection.
    def __str__(self):
        return f'There are {len(self.tasks)} task objects in the set of tasks.'

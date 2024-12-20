import Tasks as tks
import argparse



def main():
    """Main driver for the task manager program"""
    # initialize the Tasks class
    list_of_tasks = tks.Tasks()
    # use the argparse to define the add duedate delete, priority query list done and report methods
    parser = argparse.ArgumentParser(description = 'Update your To Do list.')
    parser.add_argument('--add', type=str, required=False, help='Add a task to your list by passing in a string with a name')
    parser.add_argument('--duedate', type=str, required=False, help='due date for task in MM/DD/YYYY format')
    parser.add_argument('--delete', type=int, required=False, help='delete task by id')
    parser.add_argument('--priority', type=int, required=False, default=1, help='Priority of task; default value is 1')
    parser.add_argument('--query', type=str, required=False, nargs='+', help='search for terms in the list of tasks')
    parser.add_argument('--list', action='store_true', required=False, help='List all tasks that have not been completed sorted by due date and priority')
    parser.add_argument('--done', type=int, required=False, help='Complete a task by the id')
    parser.add_argument('--report', action='store_true', required=False, help='Listing of All Tasks')
    
    # parse the argument
    args = parser.parse_args()

    # based on the argument that is passed, call the appropriate function
    if args.add:
        list_of_tasks.add(args.add, args.priority, args.duedate)
    elif args.list:
        list_of_tasks.list()
    elif args.query:
        list_of_tasks.query(args.query)
    elif args.done:
        list_of_tasks.done(args.done)
    elif args.delete:
        list_of_tasks.delete_task(args.delete)
    elif args.report:
        # for the general report function (i.e. print all tasks) pass in the list of ALL unique task ids.
        list_of_tasks.report(list_of_tasks.list_of_task_ids)
    else:
        # if it is not one of the above commands, then print the help to the user.
        parser.print_help()
    

if __name__ == '__main__':
    main()
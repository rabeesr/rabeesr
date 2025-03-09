# Task Manager Program

## Overview
This is a custom task manager program with a command line interface created by **Rabees Rafiq** for planning tasks and activities.

## Instructions
To use this program, execute the following Python file:

```bash
python3 TaskManagerDriver.py
```

## Examples of Usage
### Adding a Task
```bash
python3 TaskManagerDriver.py --add {task_name} --priority {priority} --duedate {duedate}
```
- `task_name` is required.
- `priority` and `duedate` are optional.
  - Default priority is **1** (lowest), with **3** being the highest.
  - `duedate` must be in the format `Month/Day/Year`.

### Deleting a Task
```bash
python3 TaskManagerDriver.py --delete {task_id}
```
- `task_id` must exist in the list of tasks; otherwise, an error message is returned.

### Marking a Task as Done
```bash
python3 TaskManagerDriver.py --done {task_id}
```
- `task_id` must exist in the list of tasks; otherwise, an error message is returned.
- The task's completion date is updated, and its status is set to **Done**.

### Querying for Tasks
```bash
python3 TaskManagerDriver.py --query {keyword1} {keyword2} {keyword3}...
```
- Searches the list of tasks and finds all task names matching the provided keywords.
- Case-insensitive and supports partial matches.
  - Example: A keyword of `name` will match a task named `task name 1`.

### Reporting on All Tasks
```bash
python3 TaskManagerDriver.py --report
```
- Reports all tasks, sorted by:
  1. Upcoming due dates.
  2. Priority (higher priority tasks listed first if due dates are identical).
  3. Tasks without due dates appear at the bottom.

### Reporting on Active Tasks
```bash
python3 TaskManagerDriver.py --list
```
- Reports only active tasks, following the same sorting rules as `--report`.

## Sample Task Creation Commands
Use the following commands to generate sample tasks for testing:

```bash
python3 TaskManagerDriver.py --add Task1 --priority 3 --duedate 01/15/2024
python3 TaskManagerDriver.py --add Task2
python3 TaskManagerDriver.py --add Task3 --priority 2 --duedate 08/23/2028
python3 TaskManagerDriver.py --add Task4 --duedate 11/05/2025
python3 TaskManagerDriver.py --add Task5 --priority 2
python3 TaskManagerDriver.py --add Task6
python3 TaskManagerDriver.py --add Task7 --priority 3
python3 TaskManagerDriver.py --add Task8 --duedate 06/30/2024
python3 TaskManagerDriver.py --add Task9 --priority 1
python3 TaskManagerDriver.py --add Task10 --priority 2 --duedate 06/30/2024
python3 TaskManagerDriver.py --add Task11 --priority 3 --duedate 06/30/2024
python3 TaskManagerDriver.py --add Task12 --priority 2 --duedate 11/05/2025
python3 TaskManagerDriver.py --add Task13 --priority 3 --duedate 08/23/2028
```


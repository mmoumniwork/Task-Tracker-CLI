# Task Tracker CLI
## Description
Task tracker is a project used to track and manage your tasks.
## Table of Contents
- [Task Tracker CLI](#task-tracker-cli)
  - [Description](#description)
  - [Table of Contents](#table-of-contents)
  - [Installation](#installation)
  - [Usage](#usage)
  - [Commands](#commands)
    - [This Project is part of Challanges of Roadmap.sh](#this-project-is-part-of-challanges-of-roadmapsh)

## Installation

1. Clone the repository:
   ```bash
   git clone git@github.com:mmoumniwork/Task-Tracker-CLI.git
2. Create your virtual environement
   ```bash
   python -m venv .venv
3. Install the dependencies
   ```bash
   pip install -r requirements.txt
## Usage

1. Activate your virtual environement
   ```bash
   source .venv/bin/activate
2. Run The CLI
   ```bash
   python src/main.py

## Commands
1. add new Task
   ``` bash
   Task-CLI add "task description"
2. update Task
    ``` bash
   Task-CLI update <task:id> "task description"
3. delete Task
    ``` bash
   Task-CLI delete <task:id>
4. list all Tasks
    ``` bash
   Task-CLI list
5. list tasks done
    ``` bash
   Task-CLI list done 
6. list tasks todo
    ``` bash
   Task-CLI list todo
7. list task in-progress
    ``` bash
   Task-CLI list in_progress
8. Mark a task as done
   ``` bash
   Task-CLI mark-done <task:id>
9. Mark a task in progress
    ```bash
    Task-CLI mark-in-progress <task:id>


### This Project is part of Challanges of Roadmap.sh
https://roadmap.sh/projects/task-tracker
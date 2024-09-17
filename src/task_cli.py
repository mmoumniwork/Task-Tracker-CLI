from typing import Type, Dict, Any
import os
import json
from task import Task
from parser import Parser
import logging
from datetime import datetime

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

# Create a logger
logger = logging.getLogger(__name__)


class DateTimeEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.isoformat()
        return super().default(obj)


class CLI:
    def __init__(self) -> None:
        self.filename = "data/data.json"
        self.create_json_file()
        self.data = self.load_json_data()
        self.task = Task(self)

    def create_json_file(self) -> None:
        if not os.path.isfile(self.filename):
            with open(self.filename, "w") as file:
                json.dump([], file)

    def load_json_data(self) -> Any:
        data: Any = []
        if os.path.getsize(self.filename) > 0:
            with open(self.filename, "r") as file:
                data = json.load(file)
        self.next_id = 0
        if data:
            self.next_id = int(data[-1:][0]["id"]) + 1
        return data

    def get_next_id(self):
        return self.next_id

    def increment_next_id(self):
        self.next_id += 1

    def print_data_in_json_format(self, data):
        print(json.dumps(data, indent=4, default=str))

    def add_task(self, description: str):
        try:
            self.task.create_task(description)
            with open(self.filename, "w") as file:
                json.dump(self.data, file, cls=DateTimeEncoder, indent=4)
        except Exception as e:
            logger.error(f"Error: {e}")

    def update_task(self, id: int, description=None, state=None):
        try:
            update_data = {}
            if description:
                update_data["description"] = description
            if state:
                update_data["state"] = state
            self.task.update_task(id, update_data)
            with open(self.filename, "w") as file:
                json.dump(self.data, file, cls=DateTimeEncoder, indent=4)
        except Exception as e:
            logger.error(f"Error: {e}")

    def remove_task(self, id: int):
        try:
            self.task.delete_task(id)
            with open(self.filename, "w") as file:
                json.dump(self.data, file, cls=DateTimeEncoder, indent=4)
        except Exception as e:
            logger.error(f"Error: {e}")

    def change_state(self, id: int, to_change_state: str):
        try:
            self.task.update_task(id, {"state": to_change_state})
        except Exception as e:
            logger.error(f"Error: {e}")

    def list_task(self, type: str):
        try:
            match type:
                case "all":
                    self.print_data_in_json_format(self.data)
                case "done":
                    self.print_data_in_json_format(
                        list(filter(lambda task: task["state"] == "done", self.data))
                    )
                case "todo":
                    self.print_data_in_json_format(
                        list(filter(lambda task: task["state"] == "todo", self.data))
                    )
                case "in_progress":
                    self.print_data_in_json_format(
                        list(filter(lambda task: task["state"] == "in_progress", self.data))
                    )
        except Exception as e:
            logger.error(f"Error: {e}")

    def execute_command(self, cmds: Dict[str, str]) -> None:
        try:
            match cmds["type"]:
                case "ADD":
                    self.add_task(cmds["task"])
                case "UPDATE":
                    self.update_task(int(cmds["id"]), description=cmds["task"])
                case "DELETE":
                    self.remove_task(int(cmds["id"]))
                case "MARK_IN_PROGRESS":
                    self.update_task(int(cmds["id"]), state="in_progress")
                case "MARK_DONE":
                    self.update_task(int(cmds["id"]), state="done")
                case "LIST":
                    self.list_task(cmds["CMD"])
        except Exception as e:
            logger.error(f"Error: {e}")

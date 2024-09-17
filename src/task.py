from typing import Dict, Type, List
from datetime import datetime
from pydantic import BaseModel, Field, ValidationError, model_validator
import logging


# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

# Create a logger
logger = logging.getLogger(__name__)


class TaskModel(BaseModel):
    id: int
    description: str
    state: str = Field(default="todo")
    createdAt: datetime = Field(default_factory=datetime.now)
    updatedAt: datetime = Field(default_factory=datetime.now)


class TaskUpdateModel(BaseModel):
    description: str = None
    state: str = None

    @model_validator(mode="before")
    def check_at_least_one_field(cls, data):
        if isinstance(data, dict):
            description = None
            state = None
            if "description" in data:
                description = data["description"]
            if "state" in data:
                state = data["state"]
        if not description and not state:
            raise ValueError("At least one of description or state must be provided")
        return data

    class Config:
        extra = "forbid"


class Task:
    def __init__(self, cli) -> None:
        from task_cli import CLI

        self.cli: Type[CLI] = cli

    def create_task(self, description: str) -> Dict[str, str]:
        try:
            task = TaskModel(id=self.cli.get_next_id(), description=description)
            task = dict(task)
            self.cli.data.append(task)
            self.cli.increment_next_id()
            return dict(task)
        except ValidationError as e:
            logger.error(f"Task Creation Error: {e}")

    def update_task(self, id: int, data: Dict[str, str]) -> Dict[str, str]:
        try:
            update_task = TaskUpdateModel(**data)
            try:
                int(id)
            except Exception as e:
                raise Exception(f"INVALID ID: {id}")
            task_to_update = next(
                (task for task in self.cli.data if int(task["id"]) == id), None
            )
            if not task_to_update:
                raise Exception(f"ID {id} NOT FOUND")
            if update_task.description:
                task_to_update["description"] = update_task.description
            if update_task.state:
                task_to_update["state"] = update_task.state
            task_to_update["updatedAt"] = datetime.now()
            return task_to_update
        except Exception as e:
            logger.error(f"Task Update Error: {e}")

    def delete_task(self, id: int) -> Dict[str, str]:
        try:
            try:
                int(id)
            except Exception as e:
                raise Exception(f"INVALID ID: {id}")
            task_to_delete = next(
                (task for task in self.cli.data if task["id"] == int(id)), None
            )
            if not task_to_delete:
                raise Exception(f"TASK NOT FOUND")
            self.cli.data.remove(task_to_delete)
            return task_to_delete
        except Exception as e:
            logger.error(f"Task Delete Error: {e}")

import logging
from typing import List, Dict

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

# Create a logger
logger = logging.getLogger(__name__)

COMMANDS = ["add", "update", "delete", "mark-in-progress", "mark-done", "list"]
LIST_COMMAND = ["done", "todo", "in_progress"]
TO_ADD = '\nTo add a task type: add "task_description"'
TO_UPDATE = '\nTo update a task type: update TASK_ID "task_description"'
TO_DELETE = "\nTo delete a task type: delete TASK_ID"
TO_CHANGE_STATE = (
    "\nTo change the state of a task type: mark-done/mark-in-progress TASK_ID"
)
TO_LIST = "\nTo list your tasks type: list done | todo | in-progress"


class Parser:
    """"""

    def __init__(self, args: List[str]) -> None:
        self.args: str = args

    def start(self) -> Dict[str, str]:
        if len(self.args) < 1:
            raise SystemError("System Error")
        if self.args[0] not in COMMANDS:
            raise Exception(f"INVALID COMMAND: {self.args[0]}")
        return Parser.handle_command(self.args[0], self.args[1:])
            

    @staticmethod
    def handle_command(command: str, args: List[str]) -> Dict[str, str]:
        try:
            args_len: int = len(args)
            match command:
                case "add":
                    if args_len == 0:
                        raise Exception(f"No Task Provided{TO_ADD}")
                    if args_len > 1:
                        raise Exception(f"Too Many args: {args}{TO_ADD}")
                    return dict(type="ADD", task=args[0])
                case "update":
                    if args_len != 2:
                        raise Exception(f"INVALID ARGS{TO_UPDATE}")
                    try:
                        int(args[0])
                    except Exception:
                        raise Exception(f"This ID {args[0]} is not an Integer")
                    return dict(type="UPDATE", id=args[0], task=args[1])
                case "delete":
                    if args_len != 1:
                        raise Exception(f"INVALID ARGS:{TO_DELETE}")
                    try:
                        int(args[0])
                    except Exception:
                        raise Exception(f"This ID {args[0]} is not an Integer")
                    return dict(type="DELETE", id=args[0])
                case "mark-in-progress":
                    if args_len != 1:
                        raise Exception(f"INVALID ARGS:{TO_CHANGE_STATE}")
                    try:
                        int(args[0])
                    except Exception:
                        raise Exception(f"This ID {args[0]} is not an Integer")
                    return dict(type="MARK_IN_PROGRESS", id=args[0])
                case "mark-done":
                    if args_len != 1:
                        raise Exception(f"INVALID ARGS:{TO_CHANGE_STATE}")
                    try:
                        int(args[0])
                    except Exception:
                        raise Exception(f"This ID {args[0]} is not an Integer")
                    return dict(type="MARK_DONE", id=args[0])
                case "list":
                    if args_len == 0:
                        return dict(type="LIST", CMD="all")
                    if args_len > 1:
                        raise Exception(f"INVALID ARGS:{TO_LIST}")
                    if args[0] not in LIST_COMMAND:
                        raise Exception(f"Wrong List Command: {LIST_COMMAND}")
                    return dict(type="LIST", CMD=args[0])
        except Exception as e:
            raise SyntaxError(f"Parsing Error: {e}")

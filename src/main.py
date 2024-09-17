from parser import Parser
from task_cli import CLI
import logging

RED = "\033[91m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
RESET = "\033[0m"

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)


def main(cli) -> None:
    # show a welcome interface for the user in the terminal
    while True:
        task_cli_input = input(f"{GREEN}TASK CLI: {RESET}")
        args = task_cli_input.split(" ")
        if args[0] != "":
            try:
                parser = Parser(args)
                cmds = parser.start()
                cli.execute_command(cmds)
            except Exception as e:
                logger.error(e)
        else:
            print("""Usage: TASK CLI: COMMAND Options \n\nCommands: \n\nadd <description:str>: add a Task\nupdate <id:int> <description:str>: update a Task\ndelete <id:int>: delete a Task\nmark-in-progress <id:int>: mark a task in progress state\nmark-done <id:int>: mark a task in done state\nlist: list ( done | todo | in_progress )task\n""")


if __name__ == "__main__":
    cli = CLI()
    main(cli)

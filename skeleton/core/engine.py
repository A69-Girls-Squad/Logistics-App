from core.command_factory import CommandFactory
from errors.application_error import ApplicationError


class Engine:
    """
    Main execution engine responsible for handling user input and executing commands.

    Attributes:
        _command_factory (CommandFactory): Factory instance used to create commands.

    Methods:
        start():
            Starts the command processing loop, reading user input and executing corresponding commands.
    """
    def __init__(self, factory: CommandFactory):
        """
        Initializes the Engine with a CommandFactory instance.

        Args:
            factory (CommandFactory): The factory responsible for creating command instances.
        """
        self._command_factory = factory

    def start(self):
        """
        Starts the interactive loop, processing user input and executing commands.

        The loop runs until the user enters 'exit'. Commands are processed using
        the CommandFactory, and their output is stored and displayed.

        Exceptions:
            ValueError: If an invalid command is entered, an error message is displayed.
        """
        log = ["\n"]

        while True:
            try:
                input_line = input().strip()
                if not input_line:
                    print("Please enter a command.")
                    continue
                if input_line.lower() == "exit":
                    break
                command = self._command_factory.create(input_line)
                command_output = "\n" + command.execute()
                print(command_output)
                log.append(command_output)

            except (ApplicationError, ValueError) as err:
                log.append(err.args[0])
                print(err.args[0])

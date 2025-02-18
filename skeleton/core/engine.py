from core.application_state import ApplicationState
from skeleton.core.command_factory import CommandFactory


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
        output = []

        while True:
            try:
                input_line = input()
                if input_line.lower() == 'exit':
                    break
                command = self._command_factory.create(input_line)
                output.append(command.execute())

            except ValueError as err:
                output.append(err.args[0])
                print(err.args[0])

        print('\n'.join(output))
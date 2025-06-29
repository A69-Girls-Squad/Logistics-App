from errors.application_error import ApplicationError
from core.command_factory import CommandFactory
from interface_menu import INITIAL_MENU


class Engine:
    """
    Main execution engine responsible for handling user input and executing commands.

    The Engine class processes user input, creates commands using a CommandFactory,
    and executes those commands. It runs in an interactive loop until the user enters 'exit'.

    Attributes:
        _command_factory (CommandFactory): Factory instance used to create commands.
    """
    def __init__(self, factory: CommandFactory):
        self._command_factory = factory

    def start(self):
        """
        Starts the interactive loop, processing user input and executing commands.

        The loop continuously reads user input, creates commands using the CommandFactory,
        and executes them. The output of each command is displayed, and errors are handled gracefully.

        The loop terminates when the user enters 'exit'.

        Exceptions:
            ApplicationError: If a command execution fails due to application-specific rules.
            ValueError: If an invalid command is entered or the input is malformed.
        """
        log = ["\n"]
        print(INITIAL_MENU)
        while True:
            try:
                input_command = input().strip()
                if not input_command:
                    print(INITIAL_MENU)
                    continue

                if input_command.lower() == "exit":
                    print("Exiting the application. Goodbye!")
                    break

                command = self._command_factory.create(input_command)
                command_output = "\n" + command.execute()
                print(command_output)
                log.append(command_output)

            except (ApplicationError, ValueError) as err:
                log.append(err.args[0])
                print(err.args[0])

            except KeyboardInterrupt as ki:
                print("Application terminated")

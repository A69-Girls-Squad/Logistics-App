from core.application_state import ApplicationState
from skeleton.core.command_factory import CommandFactory
from skeleton.core.engine import Engine

app_data = ApplicationState.load_data()
cmd_factory = CommandFactory(app_data)
engine = Engine(cmd_factory)

engine.start()
ApplicationState.save_data(app_data)
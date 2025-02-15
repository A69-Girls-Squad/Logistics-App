from skeleton.core.application_data import ApplicationData
from skeleton.core.command_factory import CommandFactory
from skeleton.core.engine import Engine

app_data = ApplicationData()
cmd_factory = CommandFactory(app_data)
engine = Engine(cmd_factory)

engine.start()
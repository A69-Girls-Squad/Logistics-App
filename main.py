from core.application_data import ApplicationData
from core.application_state import ApplicationState
from core.command_factory import CommandFactory
from core.engine import Engine


app_data = ApplicationState.load_data()

if app_data is None:
    app_data = ApplicationData()
    ApplicationState.seed_data(app_data)

cmd_factory = CommandFactory(app_data)
engine = Engine(cmd_factory)

engine.start()
ApplicationState.save_data(app_data)


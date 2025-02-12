import logging
from core.application_data import ApplicationData
class BaseCommand:
    def __init__(self, params, app_data: ApplicationData):
        self._params = params
        self._app_data =app_data
        self.logger = logging.getLogger(self.__class__.__name__)

    @property
    def params(self):
        return tuple(self._params)

    @property
    def app_data(self):
        return self._app_data

    def execute(self):
        # override in derived classes
        return ""

    def _expected_params_count(self) -> int:
        raise NotImplementedError('Override in derived class')


    def validate_params_count(self, params, count): # choose validate from here or from the validation_helper?
        if len(params) != count:
            raise ValueError(
                f'Invalid number of arguments. Expected: {count}; received: {len(params)}.")')


    # def _throw_if_user_logged_in(self):
    #     if self._app_data.has_logged_in_user:
    #         logged_user = self._app_data.logged_in_user
    #         raise ValueError(
    #             f'User {logged_user.username} is logged in! Please log out first!')
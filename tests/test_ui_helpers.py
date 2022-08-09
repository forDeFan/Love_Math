import pytest
from pytest_mock import mocker

from src.helpers.ui_helpers import Ui_Helpers


class Test_Ui_Helpers:

    @pytest.fixture
    def ui_hlp(self):
        return Ui_Helpers()

    def testing_widget_hiding(self, ui_hlp):
        pass

    def testing_custom_recycler(self, ui_hlp):
        pass

from pytest_mock import mocker
from src.os_helpers import Os_Helpers


class Test_Os_Helpers:
    
    def test_if_short_lang_name_returned(self):
        lang = Os_Helpers.check_lang(Os_Helpers)

        assert len(lang) == 2

    def test_if_pl_lang_detected(self):
        pl_lang = Os_Helpers.check_lang(Os_Helpers)
        
        assert pl_lang == "pl"

    def test_if_en_lang_detected(self, mocker):
        mocker.patch("locale.setlocale")
        mocker.patch("locale.getlocale", return_value=[
                     "en_En", "0", "0", "0"])
        assert "en" in Os_Helpers.check_lang(Os_Helpers)

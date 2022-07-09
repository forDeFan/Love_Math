import pytest
from src.os_helpers import Os_Helpers
import locale


class Test_Os_Helpers:
    def test_if_short_lang_name_returned(self):
        lang = Os_Helpers.check_lang(Os_Helpers)
        assert len(lang) == 2

    def test_if_pl_lang_detected(self):
        pl_lang = Os_Helpers.check_lang(Os_Helpers)
        assert pl_lang == "pl"

    @pytest.mark.skipif(
        locale.getlocale(locale.LC_MESSAGES) != "En_en",
        reason="non english OS",
    )
    def test_if_en_lang_detected(self):
        en_lang = Os_Helpers.check_lang(Os_Helpers)
        assert en_lang == "en"

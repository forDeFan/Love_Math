import locale


class Os_Helpers:
    def check_lang(self) -> str:
        locale.setlocale(locale.LC_ALL, "")
        lang = locale.getlocale(locale.LC_MESSAGES)[0][:-3]
        return lang

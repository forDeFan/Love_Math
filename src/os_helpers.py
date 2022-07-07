import locale


class Os_Helpers:
    """
    Class to interfere with os.
    """

    def check_lang(self) -> str:
        """
        Os default lang check.

        Returns:
            str: in format: "en"
        """
        locale.setlocale(locale.LC_ALL, "")
        lang = locale.getlocale(locale.LC_MESSAGES)[0][:-3]
        return lang

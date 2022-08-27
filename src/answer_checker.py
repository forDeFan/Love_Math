from kivy.clock import Clock

import src.helpers.constants as const
from src.helpers.ui_helpers import Ui_Helpers as ui_hlp


class Answer_Checker:
    """
    Class for answer check.
    """

    def good_answer(self) -> None:
        ui_hlp.change_label_ui(self, label=self.ids.result_label, l_col=const.GREEN,
                               l_out_wid="3dp", l_txt="Dobrze :)", l_f_size="30dp")
        ui_hlp.disable_widget(
            wid=self.ids.check_button, is_disabled=True
        )
        ui_hlp.hide_widget(
            self, self.ids.result_text, dohide=True
        )
        # Clear messages, generate new quest.
        Clock.schedule_once(
            lambda dt: self.new_ui_setup(),
            2,
        )

    def wrong_answer(self) -> None:
        ui_hlp.change_label_ui(self, label=self.ids.result_label, l_col=const.RED,
                               l_out_wid="0.8dp", l_txt="Żle! Spróbuj jeszcze raz", l_f_size="20dp")
        self.ids.result_text.text = ""
        ui_hlp.disable_widget(
            wid=self.ids.check_button, is_disabled=True
        )
        # Check button enable.
        Clock.schedule_once(
            lambda dt: ui_hlp.disable_widget(
                wid=self.ids.check_button, is_disabled=False
            ),
            2,
        )

    def wrong_value(self):
        ui_hlp.change_label_ui(self, label=self.ids.result_label, l_col=const.RED,
                               l_out_wid="0.8dp", l_txt="Tylko liczba!", l_f_size="20dp")
        self.ids.result_text.text = ""
        ui_hlp.disable_widget(
            wid=self.ids.check_button, is_disabled=True
        )
        # Check button enable.
        Clock.schedule_once(
            lambda dt: ui_hlp.disable_widget(
                wid=self.ids.check_button, is_disabled=False
            ),
            1,
        )
        Clock.schedule_once(
            lambda dt: self.new_ui_setup(),
            1,
        )

    def new_ui_setup(self) -> None:
        """
        Arrange UI of kv screen for new task.
        Strongly conneccted with sreen ids.

        Changes params of UI:
            result_label,
            result_text,
            check_button.
        """
        ui_hlp.disable_widget(
            wid=self.ids.check_button, is_disabled=False
        )
        ui_hlp.hide_widget(
            self, self.ids.result_text, dohide=False
        )
        ui_hlp.change_label_ui(self, label=self.ids.result_label, l_col=const.BLACK,
                               l_out_wid="0dp", l_txt="Wpisz wynik", l_f_size="15dp")
        self.ids.result_text.text = ""

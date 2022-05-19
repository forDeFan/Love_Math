from kivy.uix.screenmanager import Screen
from kivy.utils import platform

from src.db_connection import Db_Connection
from src.ui_helpers import Ui_Helpers as ui_hlp


class Results(Screen):
    def get_result(self, db: Db_Connection, category: str) -> str:
        return str(db.get_result(category)[0])

    def update_result(
        self, db: Db_Connection, category_name: str, good_answer: bool
    ):
        if good_answer:
            db.update_result(category_name)

    def hide_results(self):
        ui_hlp.hide_widget(self, wid=self.ids.results_box, dohide=True)
        ui_hlp.hide_widget(self, wid=self.ids.send_button, dohide=True)

    def show_results(self):
        self.hide_phone_book()
        self.ids.page_label.text = "Twoje wyniki"
        ui_hlp.hide_widget(self, wid=self.ids.results_box, dohide=False)
        ui_hlp.hide_widget(self, wid=self.ids.send_button, dohide=False)

    def hide_phone_book(self):
        ui_hlp.hide_widget(self, wid=self.rv, dohide=True)
        ui_hlp.hide_widget(self, wid=self.ids.results_box, dohide=True)
        ui_hlp.hide_widget(self, wid=self.ids.send_button, dohide=True)

    def show_phone_book(self):
        if platform == "android":
            from src.android_helpers import Android_Helpers as an_hlp

            ph_book = an_hlp.get_ph_book(self)
        else:
            # For non android purposes.
            ph_book = [1, 2]

        self.ids.page_label.text = "Wyślij wynik do:"
        self.hide_results()
        card = self.ids.results_card

        self.rv = ui_hlp.custom_recycle_view(
            self,
            wid_id=card,
            row_class="MDFlatButton",
            # Button events.
            data=[
                {
                    "text": str(x),
                    "theme_text_color": "Custom",
                    "text_color": (0, 0, 0, 1),
                    "on_press": lambda: ui_hlp.custom_popup(
                        self,
                        t_txt="Potwierdź",
                        c_txt="Czy wysłać wynik ?",
                        foo=lambda *args: self.send(
                            "500100900", "sending"
                        ),
                        exit_popup=False,
                        go_main_screen=False,
                        confirm=True,
                    ),
                }
                for x in ph_book
            ],
        )

    def send(self, tel, msg):
        if platform == "android":
            from src.android_helpers import Android_Helpers as an_hlp

            an_hlp.send_sms(self, tel=tel, msg=msg)
        # For non android purposes.
        print(tel, msg)
        self.show_results()

from kivy.uix.screenmanager import Screen
from kivy.utils import platform
from kivymd.uix.button import MDFlatButton

import src.constants as const
from src.db_connection import Db_Connection
from src.ui_helpers import Ui_Helpers as ui_hlp


class Results(Screen):
    def get_result(self, db: Db_Connection, category: str) -> str:
        return str(db.get_result(category)[0])

    def get_results(self, db: Db_Connection) -> str:
        r = db.get_results()
        res = ""
        for index, c in enumerate(r):
            if const.CATEGORIES[index] in c[0]:
                r = (
                    c[0].replace(
                        const.CATEGORIES[index],
                        const.CATEGORIES_PL[index],
                    )
                    + ": "
                    + str(c[1])
                    + ", "
                )
                res += r.capitalize()
        return res.rstrip(", ") + "."

    def update_result(
        self, db: Db_Connection, category_name: str, good_answer: bool
    ) -> None:
        if good_answer:
            db.update_result(category_name)

    def hide_results(self) -> None:
        ui_hlp.hide_widget(self, wid=self.ids.results_box, dohide=True)
        ui_hlp.hide_widget(self, wid=self.ids.send_button, dohide=True)

    def show_results(self) -> None:
        self.hide_phone_book()
        self.ids.page_label.text = "Twoje wyniki"
        ui_hlp.hide_widget(self, wid=self.ids.results_box, dohide=False)
        ui_hlp.hide_widget(self, wid=self.ids.send_button, dohide=False)

    def hide_phone_book(self) -> None:
        ui_hlp.hide_widget(self, wid=self.rv, dohide=True)
        ui_hlp.hide_widget(self, wid=self.ids.results_box, dohide=True)
        ui_hlp.hide_widget(self, wid=self.ids.send_button, dohide=True)

    def show_phone_book(self, db: Db_Connection) -> None:
        if platform == "android":
            from src.android_helpers import Android_Helpers as an_hlp

            ph_book = an_hlp.get_ph_book(self)
        else:
            # For non android purposes.
            ph_book = {"tata": "500100900", "mama": "900100500"}

        self.ids.page_label.text = "Wyślij wynik do:"
        self.hide_results()
        rv_wrapper = self.ids.results_card

        self.rv = ui_hlp.custom_recycle_view(
            self,
            wid=rv_wrapper,
            # Custom button class.
            rv_row_class="Rv_Button",
            # Button events for rv.
            data=[
                {  # Nem from phone book.
                    "text": name.capitalize(),
                    # Tel no.
                    "phone_no": tel,
                    # Global db to be passed to rv_button.
                    "db_obj": self.get_results(db),
                    # self = Results. To be passed to rv_button.
                    "results_obj": self,
                }
                for name, tel in ph_book.items()
            ],
        )


# Custom button class to be passed to RecycleView obj.
class Rv_Button(MDFlatButton):
    def on_press(self):
        # Confirm popup before sms.
        ui_hlp.custom_popup(
            self,
            t_txt="Potwierdź",
            c_txt="Czy wysłać wynik do "
            + self.text.capitalize()
            + " ?",
            foo=lambda *args: self.send(
                receiver_name=self.text,
                phone_no=self.phone_no,
                result=self.db_obj,
            ),
            exit_popup=False,
            go_main_screen=False,
            confirm=True,
        )

    def send(
        self, receiver_name: str, phone_no: str, result: str
    ) -> None:
        message = (
            "Hej "
            + receiver_name
            + " zobacz moje wyniki w aplikacji "
            + const.APP_NAME
            + "."
            + "\n"
            + result
        )

        if platform == "android":
            from src.android_helpers import Android_Helpers as an_hlp

            an_hlp.send_sms(self, tel=phone_no, msg=message)
        else:
            # For non android purposes.
            print("sms: ", phone_no, message)
        # Results.show_result()
        self.results_obj.show_results()

from kivy.uix.screenmanager import Screen
from kivy.utils import platform
from kivymd.uix.button import MDFlatButton

import src.constants as const
from src.db_connection import Db_Connection
from src.os_helpers import Os_Helpers as os_hlp
from src.ui_helpers import Ui_Helpers as ui_hlp

if platform == "android":
    from src.android_helpers import Android_Helpers as an_hlp


class Results(Screen):
    def get_results(self, db: Db_Connection) -> str:
        db_res = db.get_results()
        str_res = ", ".join(
            map(lambda x: x[0] + ": " + str(int(x[3])) + "%", db_res)
        )

        # TODO - sort this out.
        if " 0%" in str_res:
            str_res = str_res.replace(" 0%", " n/d")
        if " -1" in str_res:
            str_res = str_res.replace(" -1", " 0")

        for i, el in enumerate(const.CATEGORIES):
            if el in str_res:
                lang_el = const.CATEGORIES_PL[i].capitalize()

                if platform == "android":
                    if an_hlp.check_lang() == const.APP_LANG[0]:
                        str_res = str_res.replace(el, lang_el)
                    else:
                        str_res = str_res.replace(el, el.capitalize())
                else:
                    if os_hlp.check_lang(self) == const.APP_LANG[0]:
                        str_res = str_res.replace(el, lang_el)
                    else:
                        str_res = str_res.replace(el, el.capitalize())

        return str_res + "."

    def get_percentage(self, db: Db_Connection, category: str) -> str:
        per = db.get_percent(category_name=category)
        if int(per) > 0:
            return per + "%"
        elif int(per) == -1:
            return "0%"
        else:
            return "Nie zaczęto"

    def update_result(
        self, db: Db_Connection, category_name: str, good_answer: bool
    ) -> None:
        db.update_question_no(category_name=category_name)
        if good_answer:
            db.update_result(category_name)

        db.update_percent(category_name=category_name)

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
            ph_book = an_hlp.get_ph_book(self)
        else:
            # For non android purposes.
            ph_book = {
                "tata": ["500100900", "100100100"],
                "mama": "900100500",
            }

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
                {  # Name from phone book.
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
    def on_press(self) -> None:
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
            abort_button_action=lambda *args: self.results_obj.show_results(),
        )

    def send(
        self, receiver_name: str, phone_no: str, result: str
    ) -> None:
        message = (
            "Hej, "
            + receiver_name
            + " - zobacz moje wyniki w aplikacji "
            + const.APP_NAME
            + "."
        )

        if platform == "android":
            # Android sets up 70 chars limit for non en chars that's why 2 sms'es.
            an_hlp.send_sms(self, tel=phone_no[0], msg=message)
            an_hlp.send_sms(self, tel=phone_no[0], msg=result)
            an_hlp.show_toast(self, text="Wiadomość wysłana!")
        else:
            # For non android purposes.
            print("sms1: ", phone_no[0], message)
            print("sms2: ", result)
        # Results.show_result()
        self.results_obj.show_results()

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.widget import Widget


class Helpers(Widget):
    def hide_widget(self, wid, dohide=True):
        if hasattr(wid, "saved_attrs"):
            if not dohide:
                (
                    wid.height,
                    wid.size_hint_y,
                    wid.opacity,
                    wid.disabled,
                ) = wid.saved_attrs
                del wid.saved_attrs
        elif dohide:
            wid.saved_attrs = (
                wid.height,
                wid.size_hint_y,
                wid.opacity,
                wid.disabled,
            )
            wid.height, wid.size_hint_y, wid.opacity, wid.disabled = (
                0,
                None,
                0,
                True,
            )

    def custom_popup(
        self, t_txt: str, c_txt: str, foo: any, exit_popup=False
    ):
        self.box = BoxLayout(
            orientation="vertical", spacing="10px", size=(750, 750)
        )
        self.box.add_widget(Label(text=c_txt))
        self.confirm_button = Button(text="TAK")
        self.abort_button = Button(text="NIE")
        self.box.add_widget(self.confirm_button)
        self.box.add_widget(self.abort_button)

        self.pop = Popup(
            title=t_txt,
            content=self.box,
            size_hint=(None, None),
            size=(765, 755),
            auto_dismiss=False,
        )

        self.abort_button.bind(
            on_press=lambda *args: self.pop.dismiss()
        )

        if exit_popup:
            self.confirm_button.bind(on_press=lambda *args: foo.stop())
        else:
            self.confirm_button.bind(on_press=lambda *args: foo)

        self.pop.open()

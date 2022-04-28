from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.widget import Widget


class Ui_Helpers(Widget):
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
        self,
        t_txt: str,
        c_txt: str,
        foo: any,
        exit_popup=False,
        go_main_screen=False,
    ):

        self.box = BoxLayout(
            orientation="vertical", spacing="10px", size=(750, 750)
        )
        self.box.add_widget(
            Label(
                text=c_txt,
                size_hint_min_x=self.width - 30,
                size_hint_min_y=self.box.height / 2.5,
                font_size=self.height / 2.3,
                halign="center",
            )
        )

        self.confirm_button = Button(
            text="TAK",
            font_size=self.height / 1.8,
        )
        self.abort_button = Button(
            text="NIE", font_size=self.height / 1.8
        )
        self.box.add_widget(self.confirm_button)
        self.box.add_widget(self.abort_button)

        self.pop = Popup(
            title=t_txt,
            title_size=self.height / 2,
            title_align="center",
            content=self.box,
            size_hint=(None, None),
            size=(750, 750),
            auto_dismiss=False,
        )

        self.abort_button.bind(
            on_press=lambda *args: self.pop.dismiss()
        )

        # For lambda - go to main_screen.
        def go_to_main_menu(foo):
            foo.screen_manager.current = "main_screen"

        if exit_popup:
            self.confirm_button.bind(on_press=lambda *args: foo.stop())
        if go_main_screen:
            self.confirm_button.bind(
                on_press=lambda *args: self.pop.dismiss(),
                on_release=lambda *args: go_to_main_menu(foo),
            )
        else:
            foo

        self.pop.open()

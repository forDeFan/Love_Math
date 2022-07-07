from typing import List

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.recycleboxlayout import RecycleBoxLayout
from kivy.uix.recycleview import RecycleView
from kivy.uix.widget import Widget


class Ui_Helpers(Widget):
    """
    Kivi UI custom helpers.

    Args:
        Widget: needed to be passed to connect with Kivy.
    """

    def disable_widget(wid: Widget, is_disabled: bool) -> None:
        """
        Set widget interactable/ non interactable.

        Args:
            wid (Widget): widget to be disabled
            is_disabled (bool): enabled/ disbaled.
        """
        wid.disabled = is_disabled

    def hide_widget(self, wid: Widget, dohide=True) -> None:
        """
        Show/ hide widget in UI.

        Args:
            wid (Widget): widget to show/ hide
            dohide (bool, optional): hide/ show. Defaults to True - hide.
        """
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

    # TODO refactor/ atomize
    def custom_popup(
        self,
        t_txt: str,
        c_txt: str,
        foo: any,
        exit_popup=False,
        go_main_screen=False,
        confirm=False,
        abort_button_action=None,
    ) -> None:
        """
        Custom popup with user complex interaction. Reusable in UI.

        Args:
            t_txt (str): popup title text.
            c_txt (str): popup body text.
            foo (any): function to fire in popup
            exit_popup (bool, optional): if True - close the app. Defaults to False.
            go_main_screen (bool, optional): if True go to main_screen of the app. Defaults to False.
            confirm (bool, optional): if extra confirmation needed ex. at sms sending. Defaults to False.
            abort_button_action (_type_, optional): if any action needed at popup dismissal if not just close popup. Defaults to None.
        """
        content_wrapper = BoxLayout(
            orientation="vertical",
            size_hint=(1, 1),
        )
        label_wrapper = BoxLayout(
            orientation="vertical", size_hint=(1, 0.8)
        )
        button_wrapper = BoxLayout(
            orientation="vertical", spacing=15, size_hint=(1, 0.5)
        )

        label = Label(
            text=c_txt,
            size_hint=(1, 0.5),
            font_size=content_wrapper.width / 2,
            halign="center",
            pos_hint={"center_x": 0.5, "center_y": 0.5},
        )
        confirm_button = Button(
            text="TAK",
            font_size=content_wrapper.height / 1.5,
        )
        abort_button = Button(
            text="NIE",
            font_size=content_wrapper.height / 1.5,
        )

        label_wrapper.add_widget(label)
        content_wrapper.add_widget(label_wrapper)
        button_wrapper.add_widget(confirm_button)
        button_wrapper.add_widget(abort_button)
        content_wrapper.add_widget(button_wrapper)

        # Bind actions to buttons.
        if abort_button_action == None:
            abort_button.bind(on_press=lambda *args: self.pop.dismiss())
        if abort_button_action != None:

            abort_button.bind(
                on_press=lambda *args: self.pop.dismiss(),
                on_release=abort_button_action,
            )

        # Check additional conditions.
        if exit_popup:
            confirm_button.bind(on_press=lambda *args: foo.stop())
        if go_main_screen:

            def go_to_main_menu(foo):
                foo.screen_manager.current = "main_screen"

            confirm_button.bind(
                on_press=lambda *args: self.pop.dismiss(),
                on_release=lambda *args: go_to_main_menu(foo),
            )
        if confirm:
            confirm_button.bind(
                on_press=lambda *args: self.pop.dismiss(),
                on_release=foo,
            )

        self.pop = Popup(
            title=t_txt,
            title_size=content_wrapper.height / 1.5,
            title_align="center",
            content=content_wrapper,
            size_hint=(0.7, 0.5),
            auto_dismiss=False,
        )
        self.pop.open()

    def custom_recycle_view(
        self, wid: Widget, rv_row_class: str, data: List[str]
    ) -> RecycleView:
        """
        Usage of Kivy Recycle_View class for long list of items.

        Args:
            wid (Widget): in which the list will be shown.
            rv_row_class (str): widget class for every item within rv ex. button, card etc.
            data (List[str]): all data in rv. Item text from List[str].

        Returns:
            RecycleView: configured recycle_view object.
        """
        recycle_box = RecycleBoxLayout(
            default_size=(None, 80),
            default_size_hint=(1, None),
            size_hint=(1, None),
            orientation="vertical",
        )
        recycle_box.bind(minimum_height=recycle_box.setter("height"))
        recycle_view = RecycleView()
        recycle_view.data = data
        recycle_view.add_widget(recycle_box)
        recycle_view.viewclass = rv_row_class
        wid.add_widget(recycle_view)

        return recycle_view

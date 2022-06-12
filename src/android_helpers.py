from typing import Dict, List

from kvdroid.tools import toast
from kvdroid.tools.lang import device_lang
from kvdroid.tools.contact import get_contact_details
from plyer import sms


class Android_Helpers:
    def get_ph_book(self) -> Dict[str, List[str]]:
        return get_contact_details("phone_book")

    def show_toast(self, text: str) -> None:
        toast(text)

    def send_sms(self, tel: str, msg: str) -> None:
        sms.send(recipient=tel, message=msg)

    def check_lang() -> str:
        return device_lang()

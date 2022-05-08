from plyer import sms
from kvdroid.tools import toast
from kvdroid.tools.contact import get_contact_details


class Android_Helpers:
    def get_ph_book(self):
        return get_contact_details("phone_book")

    def get_ph_no(self, name):
        return get_contact_details(name)

    def show_toast(self, text):
        toast(text)

    def send_sms(self, tel, msg):
        sms.send(recipient=str(tel), message=msg)

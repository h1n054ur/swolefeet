"""CLI menu: CommunicationsMenu."""

from app.interfaces.menus.base_menu import BaseMenu
from app.use_cases.communications.send_message import SendMessage
from app.use_cases.communications.get_message_logs import GetMessageLogs
from app.use_cases.communications.make_call import MakeCall
from app.use_cases.communications.get_call_logs import GetCallLogs

class CommunicationsMenu(BaseMenu):
    def show(self):
        while True:
            self.show_header("Communications")
            print("1. Send Message")
            print("2. View Message Logs")
            print("3. Make Call")
            print("4. View Call Logs")
            print("5. Conferences (coming soon)")
            print("0. Back")

            choice = input("Select an option: ").strip()
            if choice == "1":
                from_num = input("From (e.g. +1234567890): ").strip()
                to_num = input("To (e.g. +1987654321): ").strip()
                body = input("Message Body: ").strip()
                msg = SendMessage().execute(from_num, to_num, body)
                print(f"Sent! SID: {getattr(msg, 'sid', msg)}")
            elif choice == "2":
                logs = GetMessageLogs().execute()
                print("\nRecent Messages:")
                for i, m in enumerate(logs, 1):
                    date = getattr(m, 'date_sent', '')
                    frm = getattr(m, 'from_', '')
                    to = getattr(m, 'to', '')
                    status = getattr(m, 'status', '')
                    preview = getattr(m, 'body', '')[:50]
                    print(f"{i}. {date} | {frm} -> {to} | {status} | "{preview}"")
            elif choice == "3":
                from_num = input("From (e.g. +1234567890): ").strip()
                to_num = input("To (e.g. +1987654321): ").strip()
                twiml_url = input("TwiML URL: ").strip()
                call = MakeCall().execute(from_num, to_num, twiml_url)
                print(f"Call initiated! SID: {getattr(call, 'sid', call)}")
            elif choice == "4":
                logs = GetCallLogs().execute()
                print("\nRecent Calls:")
                for i, c in enumerate(logs, 1):
                    date = getattr(c, 'start_time', '')
                    frm = getattr(c, 'from_', '')
                    to = getattr(c, 'to', '')
                    status = getattr(c, 'status', '')
                    duration = getattr(c, 'duration', '')
                    print(f"{i}. {date} | {frm} -> {to} | {status} | {duration}s")
            elif choice == "5":
                print("Conferences feature is coming soon...")
            elif choice == "0":
                break
            else:
                print("Invalid choice, please try again.")

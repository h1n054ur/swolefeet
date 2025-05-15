"""CLI menu: ActiveNumbersMenu."""

from app.interfaces.menus.base_menu import BaseMenu
from app.use_cases.numbers.view_active_numbers import ViewActiveNumbers
from app.use_cases.numbers.configure_number import ConfigureNumber
from app.use_cases.numbers.release_number import ReleaseNumber
from app.use_cases.numbers.get_number_call_logs import GetNumberCallLogs
from app.use_cases.numbers.get_number_message_logs import GetNumberMessageLogs

class ActiveNumbersMenu(BaseMenu):
    def show(self):
        viewer = ViewActiveNumbers()
        configurer = ConfigureNumber()
        releaser = ReleaseNumber()
        call_logs_uc = GetNumberCallLogs()
        msg_logs_uc = GetNumberMessageLogs()

        numbers = viewer.execute()
        while True:
            self.show_header("Manage Active Numbers")
            print(f"{'Idx':<5}{'Number':<16}{'FriendlyName':<20}")
            print("-"*45)
            for i, n in enumerate(numbers, 1):
                print(f"{i:<5}{n.phone_number:<16}{n.friendly_name:<20}")
            print("\n0. Back")
            choice = input("Select number by index: ").strip()
            if choice == "0":
                break
            if not choice.isdigit() or not (1 <= int(choice) <= len(numbers)):
                print("Invalid selection.")
                continue
            idx = int(choice) - 1
            selected = numbers[idx]

            # Sub-menu for selected number
            while True:
                self.show_header(f"Number: {selected.phone_number}")
                print("1. Configure")
                print("2. View Call Logs")
                print("3. View Message Logs")
                print("4. Release Number")
                print("0. Back")
                sub = input("Choice: ").strip()
                if sub == "1":
                    sms_url = input("New SMS URL (blank to skip): ").strip() or None
                    voice_url = input("New Voice URL (blank to skip): ").strip() or None
                    result = configurer.execute(selected.sid, sms_url=sms_url, voice_url=voice_url)
                    print(f"Updated: {result}")
                elif sub == "2":
                    logs = call_logs_uc.execute(selected.phone_number)
                    print("\nRecent Call Logs:")
                    for log in logs:
                        print(log.sid, log.from_, "->", log.to, log.status)
                    input("Press Enter to continue...")
                elif sub == "3":
                    logs = msg_logs_uc.execute(selected.phone_number)
                    print("\nRecent Message Logs:")
                    for log in logs:
                        print(log.sid, log.from_, "->", log.to, log.status)
                    input("Press Enter to continue...")
                elif sub == "4":
                    result = releaser.execute(selected.sid)
                    print("Released!" if result else "Failed to release.")
                    # Refresh list after release
                    numbers = viewer.execute()
                    break
                elif sub == "0":
                    break
                else:
                    print("Invalid choice.")

# End of ActiveNumbersMenu

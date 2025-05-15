from app.interfaces.menus.base_menu import BaseMenu

"""CLI menu: AccountMenu."""

from app.use_cases.account.get_usage_billing import GetUsageBilling
from app.use_cases.account.get_account_logs import GetAccountLogs
from app.use_cases.account.get_developer_tools import GetDeveloperTools
from app.use_cases.account.manage_subaccounts import ManageSubaccounts

class AccountMenu(BaseMenu):
    def show(self):
        while True:
            print("\nAccount Management")
            print("1. Usage & Billing")
            print("2. Developer Tools")
            print("3. Account & Subaccount Management")
            print("4. Account Logs")
            print("0. Back")

            choice = input("Select an option: ")
            if choice == "1":
                result = GetUsageBilling().execute()
                for record in result:
                    print(f"{record.description}: {record.price} {record.price_unit}")
            elif choice == "2":
                result = GetDeveloperTools().execute()
                print(result)
            elif choice == "3":
                result = ManageSubaccounts().execute()
                for acct in result:
                    print(f"{acct.friendly_name} (SID: {acct.sid})")
            elif choice == "4":
                result = GetAccountLogs().execute()
                print(result)
            elif choice == "0":
                break
            else:
                print("Invalid choice. Try again.")

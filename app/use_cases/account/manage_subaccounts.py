"""Use case: ManageSubaccounts."""

from app.services.account_service import AccountService

class ManageSubaccounts:
    def __init__(self):
        self.service = AccountService()

    def execute(self):
        return self.service.get_subaccounts()

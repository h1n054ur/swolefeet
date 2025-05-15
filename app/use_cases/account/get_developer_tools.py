"""Use case: GetDeveloperTools."""

from app.services.account_service import AccountService

class GetDeveloperTools:
    def __init__(self):
        self.service = AccountService()

    def execute(self):
        return self.service.get_api_keys()

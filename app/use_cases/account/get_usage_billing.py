"""Use case: GetUsageBilling."""

from app.services.account_service import AccountService

class GetUsageBilling:
    def __init__(self):
        self.service = AccountService()

    def execute(self):
        return self.service.get_usage_summary()

"""Service class for Account operations."""

from app.gateways.twilio_gateway import get_twilio_client

class AccountService:
    def __init__(self):
        self.client = get_twilio_client()

    def get_account_info(self):
        return self.client.api.accounts(self.client.username).fetch()

    def get_usage_summary(self):
        return self.client.usage.records.list(category="total")

    def get_subaccounts(self):
        return self.client.api.accounts.list()

    def get_api_keys(self):
        return self.client.new_keys.list()

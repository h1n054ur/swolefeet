"""Use case: SearchNumbers."""

from app.services.number_service import NumberService

class SearchNumbers:
    def __init__(self):
        self.service = NumberService()

    def execute(self, country, number_type, search_params):
        return self.service.search_numbers(country, number_type, search_params)

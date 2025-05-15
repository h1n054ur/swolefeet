"""Service class for Number operations."""

from app.gateways.twilio_gateway import get_twilio_client

class NumberService:
    def __init__(self):
        self.client = get_twilio_client()

    def get_active_numbers(self):
        return self.client.incoming_phone_numbers.list()

    def configure_number(self, sid, **kwargs):
        return self.client.incoming_phone_numbers(sid).update(**kwargs)

    def release_number(self, sid):
        return self.client.incoming_phone_numbers(sid).delete()

from app.gateways.twilio_gateway import search_available_numbers
import time

class SearchResult:
    def __init__(self, raw):
        self.phone_number = raw.get('phone_number')
        self.locality = raw.get('locality')
        self.region = raw.get('region')
        self.raw = raw

class NumberService:
    def search_numbers(self, country, number_type, search_params):
        seen = set()
        results = []
        empty_rounds = 0
        while len(results) < 500 and empty_rounds < 3:
            new_numbers = search_available_numbers(country, number_type, search_params)
            new_count = 0
            for num in new_numbers:
                if num['phone_number'] not in seen:
                    results.append(SearchResult(num))
                    seen.add(num['phone_number'])
                    new_count += 1
            if new_count == 0:
                empty_rounds += 1
            else:
                empty_rounds = 0
            time.sleep(1)
        return results

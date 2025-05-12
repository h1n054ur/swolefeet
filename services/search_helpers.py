from config.settings import ACCOUNT_SID

def build_search_url(country_code, selected_cap, digits=None, area_code=None, page=1):
    """
    Builds the appropriate Twilio API URL and parameters for search.
    """
    endpoint = "Mobile" if country_code == "AU" and selected_cap.upper() == "SMS" else "Local"
    url = f"https://api.twilio.com/2010-04-01/Accounts/{ACCOUNT_SID}/AvailablePhoneNumbers/{country_code}/{endpoint}.json"

    if digits:
        params = {
            "Contains": digits,
            f"Capabilities[{selected_cap}]": "true",
            "PageSize": 30,
            "Page": page
        }
    else:
        params = {
            f"Capabilities[{selected_cap}]": "true",
            "AreaCode": area_code,
            "PageSize": 30
        }

    return url, params


def parse_available_numbers(response, seen_set, results_list, silent=False, area_code=None):
    """
    Parses Twilio API response and appends unique numbers to result list.
    Returns the number of new entries added.
    """
    if not response or response.status_code != 200:
        return 0

    data = response.json().get("available_phone_numbers", [])
    new_count = 0

    for num in data:
        phone = num["phone_number"]
        if phone not in seen_set:
            results_list.append({
                "phone_number": phone,
                "locality": num.get("locality", "Unknown"),
                "region": num.get("region", "Unknown"),
                "capabilities": [c.upper() for c, v in num["capabilities"].items() if v]
            })
            seen_set.add(phone)
            new_count += 1

    return new_count


def should_continue_search(consecutive_empty, seen_set, max_results):
    """
    Determines whether search loop should continue based on progress.
    """
    return consecutive_empty < 2 and len(seen_set) < max_results

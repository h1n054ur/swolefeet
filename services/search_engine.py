from services.search_helpers import (
    build_search_url,
    parse_available_numbers,
    should_continue_search,
)
from config.settings import ACCOUNT_SID, API_KEY_SID, API_KEY_SECRET
from utils.storage import load_seen_numbers, clear_temp_file
from utils.ui import console
from requests.auth import HTTPBasicAuth
from rich.progress import Progress, BarColumn, TextColumn, TimeElapsedColumn, TimeRemainingColumn, MofNCompleteColumn, TaskProgressColumn
import requests
import time

auth = HTTPBasicAuth(API_KEY_SID, API_KEY_SECRET)
MAX_RESULTS = 500


def search_by_digits(country_code, selected_cap, digits, silent=False, rich_progress=None):
    clear_temp_file()
    seen_numbers = set()
    consecutive_empty = 0
    results = []
    page = 0

    task_id = None
    if rich_progress:
        task_id = rich_progress.add_task("Searching", total=MAX_RESULTS)

    while should_continue_search(consecutive_empty, seen_numbers, MAX_RESULTS):
        page += 1
        seen_numbers.update(load_seen_numbers())

        url, params = build_search_url(country_code, selected_cap, digits=digits, page=page)
        response = requests.get(url, auth=auth, params=params)

        new_numbers = parse_available_numbers(response, seen_numbers, results, silent)
        consecutive_empty = 0 if new_numbers else consecutive_empty + 1
        if rich_progress and task_id is not None:
            rich_progress.update(task_id, advance=new_numbers)

        time.sleep(0.5)

    return results


def search_by_region(country_code, selected_cap, region_data, selected_region, silent=False, rich_progress=None):
    clear_temp_file()
    seen_numbers = set()
    results = []

    task_id = None
    if rich_progress:
        task_id = rich_progress.add_task("Searching", total=MAX_RESULTS)

    area_codes = region_data[selected_region]["area_codes"]

    for area_code in area_codes:
        consecutive_empty = 0
        page = 0

        while should_continue_search(consecutive_empty, seen_numbers, MAX_RESULTS):
            page += 1
            seen_numbers.update(load_seen_numbers())

            url, params = build_search_url(country_code, selected_cap, area_code=area_code, page=page)
            response = requests.get(url, auth=auth, params=params)

            new_numbers = parse_available_numbers(response, seen_numbers, results, silent)
            consecutive_empty = 0 if new_numbers else consecutive_empty + 1
            if rich_progress and task_id is not None:
                rich_progress.update(task_id, advance=new_numbers)

            time.sleep(0.5)

    return results

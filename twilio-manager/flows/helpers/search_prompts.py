from utils.prompts import (
    prompt_country_selection,
    prompt_capability,
    prompt_search_mode,
    prompt_digit_sequence,
    prompt_region_selection
)

def get_search_parameters():
    """
    Prompt user for country, capability, and search mode (digits or region).
    Returns a tuple: (country_code, selected_capability, search_mode)
    """
    country_code = prompt_country_selection()
    if not country_code:
        return None

    selected_cap = prompt_capability()
    if selected_cap is None:
        return None

    mode = prompt_search_mode()
    if mode is None:
        return None

    search_mode = "digits" if mode else "region"
    return (country_code, selected_cap, search_mode)

def get_digit_sequence():
    """Prompt user to enter a digit sequence."""
    return prompt_digit_sequence()

def get_selected_region(country_code):
    """Prompt user to select a region for the given country."""
    return prompt_region_selection(country_code)

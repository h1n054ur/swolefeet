from rich.progress import Progress
from twilio_manager.core.phone_numbers import search_available_numbers
from twilio_manager.shared.ui.styling import (
    console,
    create_table,
    print_panel,
    print_success,
    print_error,
    print_warning,
    print_info,
    prompt_choice,
    STYLES
)

def collect_search_parameters():
    """Collect search parameters from user input.
    
    Returns:
        dict: Search parameters or None if user cancels
    """
    # Country selection
    print_panel("Select country:", style='highlight')
    console.print("1. US/Canada (+1)", style=STYLES['data'])
    console.print("2. UK (+44)", style=STYLES['data'])
    console.print("3. Australia (+61)", style=STYLES['data'])
    console.print("4. Other (specify country code)", style=STYLES['data'])
    
    country_choice = prompt_choice("Select country", choices=["1", "2", "3", "4"], default="1")
    country_codes = {
        "1": "+1",
        "2": "+44",
        "3": "+61"
    }
    
    country_code = country_codes.get(country_choice)
    if country_choice == "4":
        country_code = prompt_choice("Enter country code (with +)", choices=None)

    # Number type selection
    print_panel("Select number type:", style='highlight')
    console.print("1. Local", style=STYLES['data'])
    console.print("2. Mobile", style=STYLES['data'])
    console.print("3. Toll-Free", style=STYLES['data'])
    
    type_choice = prompt_choice("Select type", choices=["1", "2", "3"], default="1")
    number_types = {
        "1": "local",
        "2": "mobile",
        "3": "tollfree"
    }
    number_type = number_types[type_choice]

    # Capabilities selection
    print_panel("Select capabilities:", style='highlight')
    console.print("1. Voice + SMS", style=STYLES['data'])
    console.print("2. Voice only", style=STYLES['data'])
    console.print("3. SMS only", style=STYLES['data'])
    console.print("4. All (Voice + SMS + MMS)", style=STYLES['data'])
    
    caps_choice = prompt_choice("Select capabilities", choices=["1", "2", "3", "4"], default="1")
    capabilities_map = {
        "1": ["VOICE", "SMS"],
        "2": ["VOICE"],
        "3": ["SMS"],
        "4": ["VOICE", "SMS", "MMS"]
    }
    capabilities = capabilities_map[caps_choice]

    # Optional pattern
    print_panel("Number pattern (optional):", style='highlight')
    console.print("1. No pattern", style=STYLES['data'])
    console.print("2. Enter custom pattern", style=STYLES['data'])
    
    pattern_choice = prompt_choice("Select option", choices=["1", "2"], default="1")
    pattern = "" if pattern_choice == "1" else prompt_choice("Enter pattern (e.g., 555)", choices=None)

    return {
        'country_code': country_code,
        'number_type': number_type,
        'capabilities': capabilities,
        'pattern': pattern
    }

def run_number_search(params):
    """Execute the number search with the given parameters.
    
    Args:
        params (dict): Search parameters
        
    Returns:
        tuple: (results, status)
    """
    print_info("Searching...")

    # Show search criteria
    print_panel("Search criteria:", style='highlight')
    console.print("Country:", style=STYLES['dim'])
    console.print(params['country_code'], style=STYLES['info'])
    console.print("\nType:", style=STYLES['dim'])
    console.print(params['number_type'], style=STYLES['info'])
    console.print("\nCapabilities:", style=STYLES['dim'])
    console.print(', '.join(params['capabilities']), style=STYLES['info'])
    if params['pattern']:
        console.print("\nPattern:", style=STYLES['dim'])
        console.print(params['pattern'], style=STYLES['info'])

    # Initialize progress bar
    with Progress() as progress:
        search_task = progress.add_task(
            "[cyan]🔍 Searching for numbers...",
            total=500,
            description="[cyan]Searching"
        )
        
        def update_progress(count):
            progress.update(
                search_task,
                completed=min(count, 500),
                description=f"[cyan]Found {count} numbers"
            )
        
        # Search for numbers with progress tracking
        results, status = search_available_numbers(
            params['country_code'],
            params['number_type'],
            params['capabilities'],
            params['pattern'],
            progress_callback=update_progress
        )

    # Show search status
    if status.startswith("Error"):
        print_error(f"Search error: {status}")
        prompt_choice("\nPress Enter to return", choices=[""], default="")
        return None, status

    if not results:
        print_panel("No matching numbers found.", style='error')
        print_info("\nPossible reasons:")
        console.print("• No numbers available in the selected region", style=STYLES['data'])
        console.print("• No numbers match the selected capabilities", style=STYLES['data'])
        console.print("• Pattern too restrictive", style=STYLES['data'])
        console.print("• Service not available in the selected region", style=STYLES['data'])
        
        print_info("\nTry:")
        console.print("• Different region", style=STYLES['data'])
        console.print("• Fewer capabilities", style=STYLES['data'])
        console.print("• Remove pattern", style=STYLES['data'])
        
        prompt_choice("\nPress Enter to return", choices=[""], default="")
        return None, status

    print_success(status)
    return results, status

def display_search_results(results, status):
    """Display search results with pagination.
    
    Args:
        results (list): List of phone number results
        status (str): Search status message
    """
    def display_results_page(page_num: int) -> int:
        """Display a page of search results.
        
        Args:
            page_num (int): The page number to display
            
        Returns:
            int: Total number of pages
        """
        start_idx = (page_num - 1) * 50
        end_idx = min(start_idx + 50, len(results))
        total_pages = (len(results) + 49) // 50  # Round up division
        
        table = create_table(
            columns=["#", "Phone Number", "Region", "Monthly Cost", "Capabilities"],
            title=f"Found {len(results)} Available Numbers (Page {page_num}/{total_pages})"
        )
        
        for idx, number in enumerate(results[start_idx:end_idx], start_idx + 1):
            # Get capabilities
            caps = []
            if number.get('capabilities', {}).get('voice'):
                caps.append("VOICE")
            if number.get('capabilities', {}).get('sms'):
                caps.append("SMS")
            if number.get('capabilities', {}).get('mms'):
                caps.append("MMS")
            
            # Format price with currency
            price = number.get('monthlyPrice', 0)
            if isinstance(price, (int, float)):
                price_str = f"${price:.2f}"
            else:
                price_str = "—"
            
            # Add row to table
            table.add_row(
                str(idx),
                number.get("phoneNumber", "—"),
                number.get("region", "—"),
                price_str,
                " + ".join(caps) or "—",
                style=STYLES['data']
            )
        
        console.print("\n")
        console.print(table)
        
        return total_pages

    # Handle pagination and purchase options
    current_page = 1
    while True:
        total_pages = display_results_page(current_page)
        
        # Show navigation and purchase options
        print_panel("Options:", style='highlight')
        console.print("0. Return to menu", style=STYLES['data'])
        if total_pages > 1:
            if current_page > 1:
                console.print("P/p. Previous page", style=STYLES['data'])
            if current_page < total_pages:
                console.print("N/n. Next page", style=STYLES['data'])
        console.print("\nEnter a number from the list above to purchase", style=STYLES['info'])
        
        # Build choices list
        choices = ["0"]
        if total_pages > 1:
            if current_page > 1:
                choices.extend(["P", "p"])
            if current_page < total_pages:
                choices.extend(["N", "n"])
        
        # Add number choices for current page but don't show them in prompt
        start_idx = (current_page - 1) * 50
        end_idx = min(start_idx + 50, len(results))
        valid_numbers = [str(i) for i in range(start_idx + 1, end_idx + 1)]
        choices.extend(valid_numbers)
        
        selection = prompt_choice(
            "Select an option",
            choices=choices,
            show_choices=False,
            default="0"
        )
        
        if selection == "0":
            break
        elif selection.upper() == "P" and current_page > 1:
            current_page -= 1
        elif selection.upper() == "N" and current_page < total_pages:
            current_page += 1
        elif selection.isdigit():
            # Handle purchase
            selected_idx = int(selection) - 1
            from twilio_manager.cli.commands.purchase_command import handle_purchase_command
            handle_purchase_command(results[selected_idx]['phoneNumber'])
            break



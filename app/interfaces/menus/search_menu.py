"""CLI menu: SearchMenu."""

from app.interfaces.menus.base_menu import BaseMenu
from app.models.search_metadata import AREA_CODES, PRICE_TABLE, COUNTRY_NUMBER_TYPES
from app.use_cases.numbers.search_numbers import SearchNumbers
from app.use_cases.numbers.purchase_number import PurchaseNumber
from app.gateways import config
import csv, json

class SearchMenu(BaseMenu):
    def show(self):
        self.show_header('Number Search Flow')
        country_map = {'1': 'US', '2': 'CA', '3': 'GB', '4': 'AU'}
        print('Select Country:')
        print('1. US\n2. Canada\n3. UK\n4. Australia\n5. Other')
        sel = input('Choice: ').strip()
        country_code = country_map.get(sel) or input('Enter ISO-2 country code: ').strip().upper()

        types_available = COUNTRY_NUMBER_TYPES.get(country_code, ['Local'])
        print('Available types:', ', '.join(types_available))
        number_type = input('Choose type (e.g. Local): ').strip().title()
        if number_type not in types_available:
            print('Invalid type.')
            return

        print('\nSearch Mode:')
        print('1. Digits / Area Code')
        print('2. Locality')
        mode = input('Choose search mode: ').strip()
        search_params = {}

        if mode == '1':
            digits = input('Enter digits or area code: ').strip()
            if country_code == 'US' and len(digits) == 3 and digits in AREA_CODES:
                search_params['AreaCode'] = digits
            else:
                search_params['Contains'] = digits
        elif mode == '2':
            locality = input('Enter locality (e.g. New York): ').strip()
            if locality:
                search_params['InLocality'] = locality

        print('\nCapabilities:')
        print('1. Voice')
        print('2. SMS')
        print('3. Both')
        cap = input('Choose: ').strip()
        if cap == '1':
            search_params['VoiceEnabled'] = True
        elif cap == '2':
            search_params['SmsEnabled'] = True
        elif cap == '3':
            search_params['VoiceEnabled'] = True
            search_params['SmsEnabled'] = True

        print('\nSearching...')
        results = SearchNumbers().execute(country_code, number_type, search_params)

        if not results:
            print('No results found.')
            return

        def display_page(items, idx):
            print(f"\n{'Idx':<5}{'Number':<16}{'City':<20}{'State':<10}{'Type':<10}{'Price':<8}")
            print('-' * 70)
            for i, r in enumerate(items[idx:idx+50], start=idx+1):
                price = PRICE_TABLE.get(country_code, {}).get(number_type, 'N/A')
                print(f"{i:<5}{r.phone_number:<16}{r.locality or '—':<20}{r.region or country_code:<10}{number_type:<10}{price:<8}")

        index = 0
        while True:
            display_page(results, index)
            print("\nOptions: [n]ext, [p]rev, [s]ort num, [c]ity, [j]son, [v]csv, [buy] index, [q]uit")
            cmd = input('Choice: ').strip().lower()
            if cmd == 'n' and index + 50 < len(results):
                index += 50
            elif cmd == 'p' and index - 50 >= 0:
                index -= 50
            elif cmd == 's':
                results.sort(key=lambda r: r.phone_number)
                index = 0
            elif cmd == 'c':
                results.sort(key=lambda r: r.locality or '')
                index = 0
            elif cmd == 'j':
                with open('search_results.json', 'w') as f:
                    json.dump([r.raw for r in results], f, indent=2)
                print('Saved to search_results.json')
            elif cmd == 'v':
                with open('search_results.csv', 'w', newline='') as cf:
                    writer = csv.writer(cf)
                    writer.writerow(['PhoneNumber', 'City', 'State', 'Type', 'Price'])
                    for r in results:
                        writer.writerow([
                            r.phone_number,
                            r.locality,
                            r.region,
                            number_type,
                            PRICE_TABLE.get(country_code, {}).get(number_type, 'N/A')
                        ])
                print('Saved to search_results.csv')
            elif cmd.startswith('buy'):
                parts = cmd.split()
                indices = [int(i)-1 for i in parts[1:] if i.isdigit() and 1 <= int(i) <= len(results)]
                queue = [results[i].phone_number for i in indices]
                print(f'Selected: {queue}')
                if input('Confirm purchase? (y/n): ').lower() == 'y':
                    for num in queue:
                        print(PurchaseNumber().execute(num))
            elif cmd == 'q':
                break

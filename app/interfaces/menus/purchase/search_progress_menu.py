"""Menu showing search progress for available numbers."""

import asyncio
from typing import Dict, List, Optional, Set
from textual.widgets import ProgressBar, Static, DataTable
from textual.screen import Screen
from textual.containers import Vertical
from textual.binding import Binding

from ....models.phone_number_model import NumberRecord
from ....services.number_service import NumberService
from .search_results_menu import SearchResultsMenu

class SearchProgressMenu(Screen):
    """Menu showing progress while searching for available numbers."""

    BINDINGS = [
        Binding("escape", "cancel_search", "Cancel", show=True)
    ]

    def __init__(
        self,
        country_code: str,
        number_type: str,
        capabilities: Optional[List[str]] = None,
        search_pattern: Optional[str] = None,
        locality: Optional[Dict] = None,
        **kwargs
    ):
        super().__init__(**kwargs)
        self.country_code = country_code
        self.number_type = number_type
        self.capabilities = capabilities or []
        self.search_pattern = search_pattern
        self.locality = locality
        self.number_service = NumberService()
        
        # Progress tracking
        self.progress: Optional[ProgressBar] = None
        self.status: Optional[Static] = None
        self.stats: Optional[Static] = None
        self.found_numbers: Set[str] = set()
        self.search_cancelled = False
        
        # Search parameters
        self.batch_size = 50
        self.max_numbers = 500
        self.max_empty_rounds = 3
        self.empty_rounds = 0
        self.total_batches = 0
        self.total_requests = 0

    def compose(self):
        """Create child widgets."""
        yield Vertical(
            Static("Initializing search...", id="status"),
            ProgressBar(total=100, show_eta=True, id="progress"),
            Static("", id="stats"),
            id="search_container"
        )

    def on_mount(self):
        """Start search when mounted."""
        self.progress = self.query_one("#progress", ProgressBar)
        self.status = self.query_one("#status", Static)
        self.stats = self.query_one("#stats", Static)
        asyncio.create_task(self._search_numbers())

    def _update_stats(self):
        """Update search statistics."""
        self.stats.update(
            f"Found: {len(self.found_numbers)} | "
            f"Batches: {self.total_batches} | "
            f"Requests: {self.total_requests} | "
            f"Empty Rounds: {self.empty_rounds}"
        )

    async def _search_numbers(self):
        """Search for available numbers."""
        self.status.update("Starting search...")
        
        while (len(self.found_numbers) < self.max_numbers and 
               self.empty_rounds < self.max_empty_rounds and
               not self.search_cancelled):
            
            # Update progress
            progress = min(100, (len(self.found_numbers) / self.max_numbers) * 100)
            self.progress.update(progress=progress)
            
            try:
                # Search batch
                self.total_batches += 1
                self.total_requests += 1
                
                new_numbers = await self.number_service.search_available(
                    country=self.country_code,
                    type_=self.number_type,
                    capabilities=self.capabilities,
                    pattern=self.search_pattern,
                    locality=self.locality,
                    limit=self.batch_size
                )
                
                # Update status
                if not new_numbers:
                    self.empty_rounds += 1
                    self.status.update(f"No numbers found in batch {self.total_batches}")
                else:
                    self.empty_rounds = 0
                    new_count = len(new_numbers)
                    old_count = len(self.found_numbers)
                    self.found_numbers.update(num.phone_number for num in new_numbers)
                    unique_count = len(self.found_numbers) - old_count
                    
                    self.status.update(
                        f"Batch {self.total_batches}: "
                        f"Found {new_count} numbers ({unique_count} unique)"
                    )
                
                self._update_stats()
                
                # Small delay between batches
                await asyncio.sleep(1)
                
            except Exception as e:
                self.status.update(f"Error in batch {self.total_batches}: {str(e)}")
                self.empty_rounds += 1
                self._update_stats()
                await asyncio.sleep(2)
        
        # Search complete
        if not self.search_cancelled:
            await self._show_results()

    async def _show_results(self):
        """Show search results."""
        if not self.found_numbers:
            self.status.update("No numbers found")
            self._update_stats()
            await asyncio.sleep(2)
            await self.app.pop_screen()
            return
        
        # Convert to NumberRecord list
        numbers = [
            NumberRecord(
                phone_number=num,
                country=self.country_code,
                type=self.number_type,
                capabilities=self.capabilities
            )
            for num in self.found_numbers
        ]
        
        # Show results menu
        await self.app.push_screen(SearchResultsMenu(numbers=numbers))

    async def action_cancel_search(self):
        """Cancel the search."""
        self.search_cancelled = True
        self.status.update("Cancelling search...")
        self._update_stats()
        await asyncio.sleep(1)
        await self.app.pop_screen() (Rich progress bar)

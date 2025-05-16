"""Menu for confirming number purchases."""

import asyncio
from typing import Dict, List, Optional
from textual.widgets import Static, Button, DataTable
from textual.screen import Screen
from textual.containers import Vertical, Horizontal
from textual.binding import Binding

from ....models.phone_number_model import NumberRecord
from ....services.number_service import NumberService

class PurchaseConfirmMenu(Screen):
    """Menu for confirming and executing number purchases."""

    BINDINGS = [
        Binding("escape", "go_back", "Back", show=True),
        Binding("enter", "confirm_purchase", "Purchase", show=True),
        Binding("q", "toggle_queue", "Toggle Queue", show=True)
    ]

    def __init__(self, numbers: List[NumberRecord], **kwargs):
        super().__init__(**kwargs)
        self.numbers = numbers
        self.number_service = NumberService()
        self.status: Optional[Static] = None
        self.table: Optional[DataTable] = None
        self.purchase_in_progress = False
        self.use_queue = False  # Whether to use queue for purchase
        self.queue_button: Optional[Button] = None
        self.purchase_button: Optional[Button] = None

    def compose(self):
        """Create child widgets."""
        # Create table
        table = DataTable()
        table.add_columns("Number", "Type", "Capabilities", "Status")
        
        for number in self.numbers:
            capabilities = ", ".join(number.capabilities) if number.capabilities else "N/A"
            table.add_row(
                number.phone_number,
                number.type,
                capabilities,
                "Pending"
            )
        
        # Create buttons
        buttons = Horizontal(
            Button("Purchase Now", id="purchase_now", variant="primary"),
            Button("Queue Purchase", id="queue_purchase"),
            Button("Cancel", id="cancel", variant="error")
        )
        
        # Create status
        status = Static(
            f"Ready to purchase {len(self.numbers)} number(s)",
            id="status"
        )
        
        # Create purchase mode info
        mode_info = Static(
            "Purchase Mode: Immediate (press [q] to toggle queue mode)",
            id="mode_info"
        )
        
        yield Vertical(
            status,
            mode_info,
            table,
            buttons
        )

    def on_mount(self):
        """Initialize widgets when mounted."""
        self.status = self.query_one("#status", Static)
        self.table = self.query_one(DataTable)
        self.mode_info = self.query_one("#mode_info", Static)
        
        # Store button references
        self.purchase_button = self.query_one("#purchase_now", Button)
        self.queue_button = self.query_one("#queue_purchase", Button)
        
        # Set up button handlers
        self.purchase_button.on_click = self.action_confirm_purchase
        self.queue_button.on_click = self.action_confirm_purchase
        self.query_one("#cancel", Button).on_click = self.action_go_back
        
        # Update button states
        self._update_purchase_mode()

    def _update_number_status(self, index: int, status: str):
        """Update status for a number in the table."""
        if not self.table:
            return
            
        row = list(self.table.get_row(index))
        row[2] = status
        self.table.update_row(index, *row)

    def _update_purchase_mode(self):
        """Update UI elements based on purchase mode."""
        if self.use_queue:
            self.mode_info.update("Purchase Mode: Queue (press [q] to toggle immediate mode)")
            self.purchase_button.disabled = True
            self.queue_button.disabled = False
            self.queue_button.variant = "primary"
        else:
            self.mode_info.update("Purchase Mode: Immediate (press [q] to toggle queue mode)")
            self.purchase_button.disabled = False
            self.queue_button.disabled = True
            self.purchase_button.variant = "primary"

    async def action_toggle_queue(self):
        """Toggle between queue and immediate purchase."""
        if not self.purchase_in_progress:
            self.use_queue = not self.use_queue
            self._update_purchase_mode()

    async def _purchase_numbers(self):
        """Purchase all selected numbers."""
        self.purchase_in_progress = True
        
        # Update UI for purchase mode
        mode = "Queueing" if self.use_queue else "Purchasing"
        self.status.update(f"{mode} {len(self.numbers)} numbers...")
        
        try:
            if self.use_queue:
                # Queue all numbers at once
                result = await self.number_service.queue_purchase(
                    [num.phone_number for num in self.numbers]
                )
                
                if result:
                    self.status.update("✓ All numbers queued for purchase")
                    for i in range(len(self.numbers)):
                        self._update_number_status(i, "✓ Queued")
                else:
                    self.status.update("✖ Failed to queue numbers")
                    for i in range(len(self.numbers)):
                        self._update_number_status(i, "✖ Queue Failed")
                
            else:
                # Purchase numbers immediately
                for i, number in enumerate(self.numbers):
                    try:
                        # Update status
                        self._update_number_status(i, "Purchasing...")
                        self.status.update(f"Purchasing number {i+1} of {len(self.numbers)}...")
                        
                        # Purchase number
                        result = await self.number_service.purchase_number(number.phone_number)
                        
                        # Update status based on result
                        if result:
                            self._update_number_status(i, "✓ Purchased")
                        else:
                            self._update_number_status(i, "✖ Failed")
                        
                    except Exception as e:
                        self._update_number_status(i, f"✖ Error: {str(e)}")
                    
                    # Small delay between purchases
                    await asyncio.sleep(0.5)
                
                # Update final status
                self.status.update("Purchase complete")
            
        except Exception as e:
            self.status.update(f"Error: {str(e)}")
        
        self.purchase_in_progress = False
        
        # Wait before returning
        await asyncio.sleep(2)
        await self.app.pop_screen()

    async def action_go_back(self):
        """Handle back action."""
        if not self.purchase_in_progress:
            await self.app.pop_screen()

    async def action_confirm_purchase(self):
        """Handle purchase confirmation."""
        if not self.purchase_in_progress:
            await self._purchase_numbers() (confirm purchase)

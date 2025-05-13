"""Test suite for UI styling components."""

import pytest
from unittest.mock import Mock, patch
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from twilio_manager.shared.ui.styling import (
    console,
    STYLES,
    clear_screen,
    print_header,
    prompt_choice,
    print_panel,
    print_success,
    print_error,
    print_warning,
    print_info,
    create_table,
    confirm_action,
    create_spinner
)

@pytest.fixture
def mock_console():
    """Create a mock console."""
    with patch('rich.console.Console') as mock:
        console = Mock()
        mock.return_value = console
        yield console

def test_styles():
    """Test that all required styles are defined."""
    required_styles = {
        'success',
        'error',
        'warning',
        'info',
        'highlight',
        'prompt',
        'header',
        'subheader',
        'data',
        'dim'
    }
    assert set(STYLES.keys()) == required_styles

def test_print_header(mock_console):
    """Test header printing."""
    print_header("Test Title", "📦")
    mock_console.print.assert_called_with("[bold cyan]📦 Test Title[/bold cyan]\n")

def test_prompt_choice(mock_console):
    """Test choice prompting."""
    with patch('rich.prompt.Prompt.ask') as mock_ask:
        mock_ask.return_value = "1"
        result = prompt_choice("Choose:", choices=["1", "2"], default="1")
        assert result == "1"
        mock_ask.assert_called_with("Choose:", choices=["1", "2"], default="1")

def test_print_panel(mock_console):
    """Test panel printing."""
    print_panel("Test message", title="Test Title")
    mock_console.print.assert_called_once()
    args = mock_console.print.call_args[0]
    assert isinstance(args[0], Panel)
    assert args[0].title == "Test Title"

def test_print_messages(mock_console):
    """Test various print functions."""
    # Test success message
    print_success("Success!")
    mock_console.print.assert_called_with("✅ Success!", style=STYLES['success'])
    
    # Test error message
    print_error("Error!")
    mock_console.print.assert_called_with("❌ Error!", style=STYLES['error'])
    
    # Test warning message
    print_warning("Warning!")
    mock_console.print.assert_called_with("⚠️ Warning!", style=STYLES['warning'])
    
    # Test info message
    print_info("Info!")
    mock_console.print.assert_called_with("ℹ️ Info!", style=STYLES['info'])

def test_create_table():
    """Test table creation."""
    table = create_table(
        title="Test Table",
        columns=["Col1", "Col2"]
    )
    assert isinstance(table, Table)
    assert table.title == "Test Table"
    assert len(table.columns) == 2

def test_confirm_action():
    """Test action confirmation."""
    with patch('rich.prompt.Confirm.ask') as mock_ask:
        mock_ask.return_value = True
        result = confirm_action("Proceed?", default=False)
        assert result is True
        mock_ask.assert_called_with("Proceed?", default=False)

def test_create_spinner():
    """Test spinner creation."""
    spinner = create_spinner("Loading...")
    assert spinner.status == "Loading..."
    assert spinner.spinner == "dots"

def test_clear_screen(mock_console):
    """Test screen clearing."""
    clear_screen()
    mock_console.clear.assert_called_once()

def test_table_styling():
    """Test table styling consistency."""
    table = create_table(
        title="Test Table",
        columns=["Col1", "Col2"]
    )
    
    # Add some rows
    table.add_row("Data1", "Data2", style=STYLES['data'])
    table.add_row("Data3", "Data4", style=STYLES['data'])
    
    # Check column styling
    for column in table.columns:
        assert column.style == STYLES['header']

def test_panel_styling():
    """Test panel styling consistency."""
    # Test different panel styles
    print_panel("Success", style='success')
    print_panel("Error", style='error')
    print_panel("Warning", style='warning')
    print_panel("Info", style='info')
    
    # Verify all calls used correct styles
    calls = mock_console.print.call_args_list
    for call, style in zip(calls, ['success', 'error', 'warning', 'info']):
        panel = call[0][0]
        assert isinstance(panel, Panel)
        assert panel.style == STYLES[style]

def test_spinner_context():
    """Test spinner context manager."""
    with create_spinner("Loading...") as status:
        assert status.status == "Loading..."
        # Simulate work
        status.update(status="Almost done...")
        assert status.status == "Almost done..."
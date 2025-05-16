"""Test menu navigation functionality."""

import pytest
from unittest.mock import patch
from app.interfaces.menus.main_menu import MainMenu
from app.interfaces.menus.purchase.purchase_menu import PurchaseMenu
from app.interfaces.menus.manage.manage_menu import ManageMenu
from app.interfaces.menus.settings.settings_menu import SettingsMenu

def test_main_menu_creation():
    """Test main menu can be created."""
    menu = MainMenu()
    assert isinstance(menu, MainMenu)

@patch('builtins.input', side_effect=['1', 'b', 'q'])
def test_purchase_menu_navigation(mock_input):
    """Test navigation to purchase menu and back."""
    menu = MainMenu()
    with patch('os.system'):  # Mock clear screen
        menu.show()
    assert isinstance(menu, MainMenu)

@patch('builtins.input', side_effect=['2', 'b', 'q'])
def test_manage_menu_navigation(mock_input):
    """Test navigation to manage menu and back."""
    menu = MainMenu()
    with patch('os.system'):  # Mock clear screen
        menu.show()
    assert isinstance(menu, MainMenu)

@patch('builtins.input', side_effect=['3', 'b', 'q'])
def test_settings_menu_navigation(mock_input):
    """Test navigation to settings menu and back."""
    menu = MainMenu()
    with patch('os.system'):  # Mock clear screen
        menu.show()
    assert isinstance(menu, MainMenu)

def test_menu_parent_child_relationship():
    """Test parent-child menu relationships."""
    main = MainMenu()
    purchase = PurchaseMenu(parent=main)
    manage = ManageMenu(parent=main)
    settings = SettingsMenu(parent=main)
    
    assert purchase.parent == main
    assert manage.parent == main
    assert settings.parent == main
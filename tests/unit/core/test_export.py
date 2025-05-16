"""Tests for file export functionality."""

import pytest
import json
import csv
import tempfile
import os
from datetime import datetime
from app.core.export import export_to_json, export_to_csv
from app.models.phone_number import PhoneNumber

@pytest.mark.core
class TestExport:
    """Test suite for export functionality."""
    
    @pytest.fixture
    def sample_numbers(self):
        """Create a sample list of phone numbers."""
        return [
            PhoneNumber(
                number="+15550001111",
                friendly_name='Test "1"',  # Test quote escaping
                city="Atlanta, GA",  # Test comma escaping
                state="GA",
                country="US",
                capabilities={"voice": True, "sms": True},
                added_at=datetime(2023, 1, 1, 12, 0)
            ),
            PhoneNumber(
                number="+15550002222",
                friendly_name="Test 2",
                city="Boston",
                state="MA",
                country="US",
                capabilities={"voice": False, "sms": True},
                added_at=datetime(2023, 1, 2, 12, 0)
            )
        ]
    
    def test_json_export(self, sample_numbers):
        """Test exporting to JSON format."""
        with tempfile.NamedTemporaryFile(suffix='.json', delete=False) as temp:
            try:
                # Export to JSON
                export_to_json(sample_numbers, temp.name)
                
                # Read and verify JSON
                with open(temp.name, 'r') as f:
                    data = json.load(f)
                
                assert len(data) == 2
                assert data[0]['number'] == "+15550001111"
                assert data[0]['friendly_name'] == 'Test "1"'
                assert data[0]['capabilities'] == {"voice": True, "sms": True}
                assert data[1]['number'] == "+15550002222"
                assert data[1]['capabilities'] == {"voice": False, "sms": True}
                
            finally:
                os.unlink(temp.name)
    
    def test_csv_export(self, sample_numbers):
        """Test exporting to CSV format."""
        with tempfile.NamedTemporaryFile(suffix='.csv', delete=False) as temp:
            try:
                # Export to CSV
                export_to_csv(sample_numbers, temp.name)
                
                # Read and verify CSV
                with open(temp.name, 'r', newline='') as f:
                    reader = csv.DictReader(f)
                    rows = list(reader)
                
                assert len(rows) == 2
                
                # Verify headers
                expected_headers = [
                    'number', 'friendly_name', 'city', 'state', 'country',
                    'voice_enabled', 'sms_enabled', 'added_at'
                ]
                assert reader.fieldnames == expected_headers
                
                # Verify first row
                assert rows[0]['number'] == '+15550001111'
                assert rows[0]['friendly_name'] == 'Test "1"'
                assert rows[0]['city'] == 'Atlanta, GA'
                assert rows[0]['voice_enabled'] == 'True'
                assert rows[0]['sms_enabled'] == 'True'
                
                # Verify second row
                assert rows[1]['number'] == '+15550002222'
                assert rows[1]['friendly_name'] == 'Test 2'
                assert rows[1]['city'] == 'Boston'
                assert rows[1]['voice_enabled'] == 'False'
                assert rows[1]['sms_enabled'] == 'True'
                
            finally:
                os.unlink(temp.name)
    
    def test_json_export_empty_list(self):
        """Test exporting an empty list to JSON."""
        with tempfile.NamedTemporaryFile(suffix='.json', delete=False) as temp:
            try:
                export_to_json([], temp.name)
                
                with open(temp.name, 'r') as f:
                    data = json.load(f)
                
                assert data == []
                
            finally:
                os.unlink(temp.name)
    
    def test_csv_export_empty_list(self):
        """Test exporting an empty list to CSV."""
        with tempfile.NamedTemporaryFile(suffix='.csv', delete=False) as temp:
            try:
                export_to_csv([], temp.name)
                
                with open(temp.name, 'r', newline='') as f:
                    reader = csv.DictReader(f)
                    rows = list(reader)
                
                # Should have headers but no rows
                assert reader.fieldnames is not None
                assert len(rows) == 0
                
            finally:
                os.unlink(temp.name)
    
    def test_json_export_special_chars(self):
        """Test JSON export with special characters."""
        numbers = [
            PhoneNumber(
                number="+15550001111",
                friendly_name="Test\nNewline",  # Test newline
                city="City\\Slash",  # Test backslash
                state="ST",
                country="US",
                capabilities={"voice": True, "sms": True},
                added_at=datetime.now()
            )
        ]
        
        with tempfile.NamedTemporaryFile(suffix='.json', delete=False) as temp:
            try:
                export_to_json(numbers, temp.name)
                
                with open(temp.name, 'r') as f:
                    data = json.load(f)
                
                assert data[0]['friendly_name'] == "Test\nNewline"
                assert data[0]['city'] == "City\\Slash"
                
            finally:
                os.unlink(temp.name)
    
    def test_csv_export_special_chars(self):
        """Test CSV export with special characters."""
        numbers = [
            PhoneNumber(
                number="+15550001111",
                friendly_name='Test,Comma"Quote',  # Test comma and quote
                city="City\nNewline",  # Test newline
                state="ST",
                country="US",
                capabilities={"voice": True, "sms": True},
                added_at=datetime.now()
            )
        ]
        
        with tempfile.NamedTemporaryFile(suffix='.csv', delete=False) as temp:
            try:
                export_to_csv(numbers, temp.name)
                
                with open(temp.name, 'r', newline='') as f:
                    reader = csv.DictReader(f)
                    row = next(reader)
                
                assert row['friendly_name'] == 'Test,Comma"Quote'
                assert row['city'] == "City\nNewline"
                
            finally:
                os.unlink(temp.name)
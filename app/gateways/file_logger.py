"""File-based logging gateway for operation tracking and debugging."""

import json
import logging
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, Optional, List

logger = logging.getLogger(__name__)

class FileLogger:
    """JSON file-based logger for tracking operations and debugging."""
    
    def __init__(self, log_dir: str = "logs"):
        """Initialize the file logger.
        
        Args:
            log_dir: Directory to store log files. Created if doesn't exist.
        """
        self.log_dir = Path(log_dir)
        self.log_dir.mkdir(exist_ok=True)
        
        # Initialize log files
        self.operation_log = self.log_dir / "operations.json"
        self.search_log = self.log_dir / "searches.json"
        self.debug_log = self.log_dir / "debug.json"
        
        # Create files if they don't exist
        for log_file in [self.operation_log, self.search_log, self.debug_log]:
            if not log_file.exists():
                log_file.write_text("[]")

    def _append_to_log(self, log_file: Path, entry: Dict[str, Any]) -> None:
        """Append a new entry to a JSON log file.
        
        Args:
            log_file: Path to the log file
            entry: Dictionary containing the log entry
        """
        try:
            # Read existing logs
            with log_file.open('r') as f:
                logs = json.load(f)
            
            # Add timestamp and append
            entry["timestamp"] = datetime.utcnow().isoformat()
            logs.append(entry)
            
            # Write back to file
            with log_file.open('w') as f:
                json.dump(logs, f, indent=2)
                
        except Exception as e:
            logger.error(f"Failed to write to log file {log_file}: {e}")

    def log_operation(self, operation: str, number: str,
                     status: str = "success",
                     details: Optional[Dict] = None) -> None:
        """Log a phone number operation.
        
        Args:
            operation: Type of operation (purchase, release, etc.)
            number: Phone number involved
            status: Operation status (success/failed)
            details: Additional operation details
        """
        entry = {
            "operation": operation,
            "number": number,
            "status": status,
            "details": details or {}
        }
        self._append_to_log(self.operation_log, entry)

    def log_search(self, country: str, type_: str,
                  capabilities: Optional[Dict] = None,
                  results_count: int = 0) -> None:
        """Log a phone number search operation.
        
        Args:
            country: Country code searched
            type_: Number type (local/mobile/toll-free)
            capabilities: Required capabilities
            results_count: Number of results found
        """
        entry = {
            "operation": "search",
            "country": country,
            "type": type_,
            "capabilities": capabilities or {},
            "results_count": results_count
        }
        self._append_to_log(self.search_log, entry)

    def log_debug(self, component: str, action: str,
                 data: Optional[Dict] = None) -> None:
        """Log debug information.
        
        Args:
            component: System component (gateway/service name)
            action: Action being performed
            data: Debug data to log
        """
        entry = {
            "component": component,
            "action": action,
            "data": data or {}
        }
        self._append_to_log(self.debug_log, entry)

    def get_recent_operations(self, limit: int = 100,
                            operation_type: Optional[str] = None) -> List[Dict]:
        """Get recent operations from the log.
        
        Args:
            limit: Maximum number of operations to return
            operation_type: Filter by operation type
            
        Returns:
            List of operation log entries
        """
        try:
            with self.operation_log.open('r') as f:
                logs = json.load(f)
            
            if operation_type:
                logs = [log for log in logs if log["operation"] == operation_type]
            
            return logs[-limit:]
            
        except Exception as e:
            logger.error(f"Failed to read operation logs: {e}")
            return []

    def get_search_history(self, limit: int = 100,
                         country: Optional[str] = None) -> List[Dict]:
        """Get recent search operations.
        
        Args:
            limit: Maximum number of searches to return
            country: Filter by country code
            
        Returns:
            List of search log entries
        """
        try:
            with self.search_log.open('r') as f:
                logs = json.load(f)
            
            if country:
                logs = [log for log in logs if log["country"] == country]
            
            return logs[-limit:]
            
        except Exception as e:
            logger.error(f"Failed to read search logs: {e}")
            return []

    def get_debug_logs(self, limit: int = 100,
                      component: Optional[str] = None) -> List[Dict]:
        """Get recent debug logs.
        
        Args:
            limit: Maximum number of logs to return
            component: Filter by component name
            
        Returns:
            List of debug log entries
        """
        try:
            with self.debug_log.open('r') as f:
                logs = json.load(f)
            
            if component:
                logs = [log for log in logs if log["component"] == component]
            
            return logs[-limit:]
            
        except Exception as e:
            logger.error(f"Failed to read debug logs: {e}")
            return []

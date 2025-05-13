from twilio_manager.core.messaging import get_message_logs
from twilio_manager.core.voice import get_call_logs

def get_message_logs_list():
    """Get list of message logs.
    
    Returns:
        list: List of message log entries
    """
    return get_message_logs()

def get_call_logs_list():
    """Get list of call logs.
    
    Returns:
        list: List of call log entries
    """
    return get_call_logs()

def format_message_log_entry(log):
    """Format a single message log entry.
    
    Args:
        log (dict): Message log entry
        
    Returns:
        dict: Formatted log entry
    """
    return {
        'from': log.get("from", "—"),
        'to': log.get("to", "—"),
        'body': log.get("body", "")[:40] + "...",
        'status': log.get("status", "—"),
        'date_sent': log.get("date_sent", "—")
    }

def format_call_log_entry(log):
    """Format a single call log entry.
    
    Args:
        log (dict): Call log entry
        
    Returns:
        dict: Formatted log entry
    """
    return {
        'from': log.get("from", "—"),
        'to': log.get("to", "—"),
        'status': log.get("status", "—"),
        'duration': str(log.get("duration", "0")),
        'start_time': log.get("start_time", "—")
    }

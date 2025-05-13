from twilio.rest import Client
from twilio_manager.shared.config import ACCOUNT_SID, AUTH_TOKEN

client = Client(ACCOUNT_SID, AUTH_TOKEN)

def send_message_api(from_number, to_number, body) -> tuple[bool, str | None]:
    """Send a message using Twilio API.
    
    Args:
        from_number (str): Sender phone number
        to_number (str): Recipient phone number
        body (str): Message content
        
    Returns:
        tuple[bool, str | None]: (success, error_message)
    """
    try:
        message = client.messages.create(
            from_=from_number,
            to=to_number,
            body=body
        )
        return bool(message and message.sid), None
    except Exception as e:
        return False, str(e)

def fetch_message_logs_api(limit=20) -> tuple[list, str | None]:
    """Fetch message logs from Twilio API.
    
    Args:
        limit (int): Maximum number of logs to fetch
        
    Returns:
        tuple[list, str | None]: (message_logs, error_message)
    """
    try:
        messages = client.messages.list(limit=limit)
        logs = [
            {
                "from": m.from_,
                "to": m.to,
                "body": m.body,
                "status": m.status,
                "date_sent": str(m.date_sent)
            } for m in messages
        ]
        return logs, None
    except Exception as e:
        return [], str(e)

def get_recent_contacts_api(limit=10) -> tuple[list, str | None]:
    """Get a list of unique recent contacts from message history.
    
    Args:
        limit (int): Maximum number of contacts to return
        
    Returns:
        tuple[list, str | None]: (contacts_list, error_message)
    """
    try:
        messages = client.messages.list(limit=100)  # Get more messages to find unique contacts
        contacts = {}
        
        for msg in messages:
            # If this is an outgoing message, add the recipient
            if msg.direction == 'outbound-api':
                if msg.to not in contacts:
                    contacts[msg.to] = {
                        'phoneNumber': msg.to,
                        'lastContact': str(msg.date_sent),
                        'lastDirection': 'outbound'
                    }
            # If this is an incoming message, add the sender
            else:
                if msg.from_ not in contacts:
                    contacts[msg.from_] = {
                        'phoneNumber': msg.from_,
                        'lastContact': str(msg.date_sent),
                        'lastDirection': 'inbound'
                    }
            
            # Break if we have enough unique contacts
            if len(contacts) >= limit:
                break
        
        return list(contacts.values())[:limit], None
    except Exception as e:
        return [], str(e)

from twilio.rest import Client
from twilio_manager.shared.config import ACCOUNT_SID, AUTH_TOKEN

client = Client(ACCOUNT_SID, AUTH_TOKEN)

def send_message_api(from_number, to_number, body):
    try:
        message = client.messages.create(
            from_=from_number,
            to=to_number,
            body=body
        )
        return bool(message and message.sid)
    except Exception as e:
        print(f"[service] Failed to send message: {e}")
        return False

def fetch_message_logs_api(limit=20):
    try:
        messages = client.messages.list(limit=limit)
        return [
            {
                "from": m.from_,
                "to": m.to,
                "body": m.body,
                "status": m.status,
                "date_sent": str(m.date_sent)
            } for m in messages
        ]
    except Exception as e:
        print(f"[service] Failed to fetch message logs: {e}")
        return []


def get_recent_contacts_api(limit=10):
    """Get a list of unique recent contacts from message history."""
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
        
        return list(contacts.values())[:limit]
    except Exception as e:
        print(f"[service] Failed to get recent contacts: {e}")
        return []

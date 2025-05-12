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

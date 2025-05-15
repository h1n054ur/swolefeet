from typing import Dict, Optional
import logging
from datetime import datetime, timedelta
from ..gateways.twilio_gateway import TwilioGateway
from ..models.account_model import UsageStats

logger = logging.getLogger(__name__)

class AccountService:
    def __init__(self, twilio_gateway: TwilioGateway):
        self.twilio_gateway = twilio_gateway

    def get_usage(self, days: int = 30) -> UsageStats:
        """
        Get usage statistics for the specified time period.
        Returns UsageStats with usage metrics and costs.
        """
        try:
            client = self.twilio_gateway.get_client()
            
            # Calculate date range
            end_date = datetime.utcnow()
            start_date = end_date - timedelta(days=days)
            
            # Get usage records
            records = client.usage.records.list(
                start_date=start_date.date(),
                end_date=end_date.date()
            )
            
            # Calculate totals
            total_cost = sum(float(record.price) for record in records)
            usage_by_category = {
                record.category: {
                    "usage": record.usage,
                    "units": record.usage_unit,
                    "cost": float(record.price)
                }
                for record in records
            }
            
            # Project monthly cost based on current usage
            daily_avg = total_cost / days
            monthly_projection = daily_avg * 30
            
            return UsageStats(
                usage=usage_by_category,
                cost=total_cost,
                projection=monthly_projection
            )
            
        except Exception as e:
            logger.error(f"Failed to get usage statistics: {e}")
            return UsageStats(usage={}, cost=0.0, projection=0.0)

    def get_billing(self) -> Dict:
        """
        Get billing information including current balance and last payment.
        """
        try:
            client = self.twilio_gateway.get_client()
            
            # Get balance
            balance = client.api.balance.fetch()
            
            # Get recent charges
            charges = client.api.balance.last_month.fetch()
            
            return {
                "balance": float(balance.balance),
                "currency": balance.currency,
                "last_month_charges": float(charges.total),
                "last_month_usage": float(charges.usage_charges),
                "last_month_fees": float(charges.total_fee)
            }
            
        except Exception as e:
            logger.error(f"Failed to get billing information: {e}")
            return {
                "balance": 0.0,
                "currency": "USD",
                "last_month_charges": 0.0,
                "last_month_usage": 0.0,
                "last_month_fees": 0.0
            }

    def get_account_logs(self, page_token: Optional[str] = None) -> Dict:
        """
        Get account-wide logs (calls and messages).
        Supports pagination.
        """
        try:
            # Get both call and message logs
            call_logs = self.twilio_gateway.list_logs("calls", page_token=page_token)
            message_logs = self.twilio_gateway.list_logs("messages", page_token=page_token)
            
            # Combine and sort by timestamp
            all_logs = []
            all_logs.extend([{
                "type": "call",
                "timestamp": log.start_time,
                "from": log.from_,
                "to": log.to,
                "status": log.status,
                "duration": log.duration,
                "price": float(log.price or 0)
            } for log in call_logs["items"]])
            
            all_logs.extend([{
                "type": "message",
                "timestamp": log.date_created,
                "from": log.from_,
                "to": log.to,
                "status": log.status,
                "body": log.body,
                "price": float(log.price or 0)
            } for log in message_logs["items"]])
            
            # Sort by timestamp descending
            all_logs.sort(key=lambda x: x["timestamp"], reverse=True)
            
            return {
                "items": all_logs,
                "next_page_token": call_logs.get("next_page_token") or message_logs.get("next_page_token")
            }
            
        except Exception as e:
            logger.error(f"Failed to get account logs: {e}")
            return {
                "items": [],
                "next_page_token": None
            }

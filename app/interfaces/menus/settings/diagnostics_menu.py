"""Menu for system diagnostics and monitoring."""

import logging
from typing import Dict, Callable
from datetime import datetime, timedelta
from rich.table import Table
from ..base_menu import BaseMenu
from ....services.diagnostics_service import DiagnosticsService

logger = logging.getLogger(__name__)

class DiagnosticsMenu(BaseMenu):
    """Menu for system diagnostics and monitoring."""
    
    def __init__(self, parent: BaseMenu = None):
        """Initialize the menu.
        
        Args:
            parent: Optional parent menu for navigation.
        """
        super().__init__(parent)
        self.diagnostics_service = DiagnosticsService()
    
    def show(self) -> None:
        """Display the diagnostics menu."""
        self.clear_screen()
        self.render_header("System Diagnostics")
        
        options: Dict[str, Callable] = {
            '1': self.show_webhook_failures,
            '2': self.show_rate_limits,
            '3': self.show_system_health,
            '4': self.show_api_latency,
            '5': self.show_error_trends
        }
        
        while self.prompt_choice(options):
            self.clear_screen()
            self.render_header("System Diagnostics")
    
    def show_webhook_failures(self) -> bool:
        """Show webhook failure events.
        
        Returns:
            True to continue menu loop.
        """
        try:
            # Get webhook failures
            failures = self.diagnostics_service.get_webhook_failures(
                start_date=datetime.now() - timedelta(days=7)
            )
            
            if not failures:
                self.console.print("[yellow]No webhook failures found![/yellow]")
                return True
            
            table = Table(show_header=True, header_style="bold blue")
            table.add_column("Time")
            table.add_column("URL")
            table.add_column("Status")
            table.add_column("Error")
            table.add_column("Response")
            
            for failure in failures:
                table.add_row(
                    failure.timestamp.strftime("%Y-%m-%d %H:%M:%S"),
                    failure.url[:50] + "..." if len(failure.url) > 50 else failure.url,
                    str(failure.status_code),
                    failure.error_type,
                    failure.response[:50] + "..." if failure.response and len(failure.response) > 50 else failure.response or ""
                )
            
            self.console.print("\n[bold]Recent Webhook Failures[/bold]")
            self.console.print(table)
            
            return True
            
        except Exception as e:
            logger.exception("Error showing webhook failures")
            self.console.print(f"[red]Error: {str(e)}[/red]")
            return True
    
    def show_rate_limits(self) -> bool:
        """Show rate limit events and current status.
        
        Returns:
            True to continue menu loop.
        """
        try:
            # Get rate limit info
            limits = self.diagnostics_service.get_rate_limits()
            
            self.console.print("\n[bold]Current Rate Limits[/bold]")
            
            # Show current limits
            table = Table(show_header=True, header_style="bold blue")
            table.add_column("API")
            table.add_column("Limit")
            table.add_column("Used")
            table.add_column("Remaining")
            table.add_column("Reset Time")
            
            for limit in limits.current:
                table.add_row(
                    limit.api,
                    str(limit.limit),
                    str(limit.used),
                    str(limit.remaining),
                    limit.reset_time.strftime("%H:%M:%S")
                )
            
            self.console.print(table)
            
            # Show recent breaches
            if limits.breaches:
                breach_table = Table(show_header=True, header_style="bold red")
                breach_table.add_column("Time")
                breach_table.add_column("API")
                breach_table.add_column("Duration")
                breach_table.add_column("Impact")
                
                for breach in limits.breaches:
                    breach_table.add_row(
                        breach.timestamp.strftime("%Y-%m-%d %H:%M:%S"),
                        breach.api,
                        str(breach.duration_seconds) + "s",
                        breach.impact
                    )
                
                self.console.print("\n[bold red]Recent Rate Limit Breaches[/bold red]")
                self.console.print(breach_table)
            
            return True
            
        except Exception as e:
            logger.exception("Error showing rate limits")
            self.console.print(f"[red]Error: {str(e)}[/red]")
            return True
    
    def show_system_health(self) -> bool:
        """Show system health metrics.
        
        Returns:
            True to continue menu loop.
        """
        try:
            # Get health metrics
            health = self.diagnostics_service.get_system_health()
            
            self.console.print("\n[bold]System Health[/bold]")
            
            # Show service status
            service_table = Table(show_header=True, header_style="bold blue")
            service_table.add_column("Service")
            service_table.add_column("Status")
            service_table.add_column("Latency")
            service_table.add_column("Uptime")
            
            for service in health.services:
                status_color = "green" if service.status == "Healthy" else "red"
                service_table.add_row(
                    service.name,
                    f"[{status_color}]{service.status}[/{status_color}]",
                    f"{service.latency_ms}ms",
                    f"{service.uptime_percentage}%"
                )
            
            self.console.print(service_table)
            
            # Show resource usage
            self.console.print("\n[bold]Resource Usage[/bold]")
            self.console.print(f"CPU: {health.cpu_usage}%")
            self.console.print(f"Memory: {health.memory_usage}%")
            self.console.print(f"Storage: {health.storage_usage}%")
            
            # Show alerts
            if health.alerts:
                self.console.print("\n[bold red]Active Alerts[/bold red]")
                for alert in health.alerts:
                    self.console.print(f"- {alert}")
            
            return True
            
        except Exception as e:
            logger.exception("Error showing system health")
            self.console.print(f"[red]Error: {str(e)}[/red]")
            return True
    
    def show_api_latency(self) -> bool:
        """Show API latency metrics.
        
        Returns:
            True to continue menu loop.
        """
        try:
            # Get latency metrics
            metrics = self.diagnostics_service.get_api_latency()
            
            table = Table(show_header=True, header_style="bold blue")
            table.add_column("API")
            table.add_column("Avg (ms)")
            table.add_column("Min (ms)")
            table.add_column("Max (ms)")
            table.add_column("p95 (ms)")
            table.add_column("Errors")
            
            for metric in metrics:
                table.add_row(
                    metric.api,
                    str(metric.avg_latency),
                    str(metric.min_latency),
                    str(metric.max_latency),
                    str(metric.p95_latency),
                    f"{metric.error_rate}%"
                )
            
            self.console.print("\n[bold]API Latency Metrics[/bold]")
            self.console.print("Last 24 hours")
            self.console.print(table)
            
            return True
            
        except Exception as e:
            logger.exception("Error showing API latency")
            self.console.print(f"[red]Error: {str(e)}[/red]")
            return True
    
    def show_error_trends(self) -> bool:
        """Show error trends and patterns.
        
        Returns:
            True to continue menu loop.
        """
        try:
            # Get error trends
            trends = self.diagnostics_service.get_error_trends()
            
            if not trends:
                self.console.print("[yellow]No error trends found![/yellow]")
                return True
            
            table = Table(show_header=True, header_style="bold blue")
            table.add_column("Error Type")
            table.add_column("Count")
            table.add_column("First Seen")
            table.add_column("Last Seen")
            table.add_column("Trend")
            table.add_column("Impact")
            
            for trend in trends:
                table.add_row(
                    trend.error_type,
                    str(trend.count),
                    trend.first_seen.strftime("%Y-%m-%d %H:%M"),
                    trend.last_seen.strftime("%Y-%m-%d %H:%M"),
                    trend.trend_direction,
                    trend.impact_level
                )
            
            self.console.print("\n[bold]Error Trends[/bold]")
            self.console.print("Last 7 days")
            self.console.print(table)
            
            # Show recommendations
            if trends[0].recommendations:
                self.console.print("\n[bold]Recommendations[/bold]")
                for rec in trends[0].recommendations:
                    self.console.print(f"- {rec}")
            
            return True
            
        except Exception as e:
            logger.exception("Error showing error trends")
            self.console.print(f"[red]Error: {str(e)}[/red]")
            return True
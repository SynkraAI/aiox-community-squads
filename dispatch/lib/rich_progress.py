"""
Rich-based live progress dashboards for dispatch squad.

Provides live updating progress display with colors, spinners, and
formatted tables. Falls back to plain text if Rich is not available.
"""

import time
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any

# Try to import Rich components
try:
    from rich.live import Live
    from rich.table import Table
    from rich.panel import Panel
    from rich.progress import Progress, BarColumn, TextColumn, TimeElapsedColumn
    from rich.console import Console, Group
    from rich.text import Text
    from rich import box
    from rich.spinner import Spinner
    RICH_AVAILABLE = True
except ImportError:
    RICH_AVAILABLE = False


# Status icons and colors
STATUS_ICONS = {
    "pending": ("⏳", "dim"),
    "queued": ("📋", "cyan"),
    "executing": ("⚡", "yellow"),
    "pass": ("✅", "green"),
    "fail": ("❌", "red"),
    "retry": ("🔄", "yellow"),
}


class DispatchDashboard:
    """Live dispatch monitoring dashboard using Rich."""

    def __init__(self, run_id: str, total_tasks: int, total_waves: int):
        if not RICH_AVAILABLE:
            raise ImportError("Rich library required for live dashboard. Install: pip install rich")

        self.run_id = run_id
        self.total_tasks = total_tasks
        self.total_waves = total_waves
        self.current_wave = 0
        self.current_phase = "Initializing"
        self.total_cost = 0.0
        self.start_time = None

        # Task tracking
        self.tasks: Dict[str, Dict[str, Any]] = {}
        self.wave_status: Dict[int, Dict[str, Any]] = {}

        # Rich components
        self.console = Console()
        self.live = None
        self.logs: List[str] = []

    def start(self):
        """Start live display."""
        self.start_time = datetime.now()
        self.live = Live(self._generate_layout(), refresh_per_second=4, console=self.console)
        self.live.start()
        return self

    def stop(self):
        """Stop live display."""
        if self.live:
            self.live.stop()

    def __enter__(self):
        """Context manager entry."""
        return self.start()

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.stop()

    def update_task(self, task_id: str, status: str, description: str = "",
                    tokens: int = 0, cost: float = 0.0):
        """Update a task's status in the dashboard."""
        if task_id not in self.tasks:
            self.tasks[task_id] = {
                "description": description,
                "status": status,
                "tokens": 0,
                "cost": 0.0,
                "error": None,
            }

        self.tasks[task_id]["status"] = status
        if description:
            self.tasks[task_id]["description"] = description
        if tokens > 0:
            self.tasks[task_id]["tokens"] = tokens
        if cost > 0:
            self.tasks[task_id]["cost"] = cost
            self.total_cost += cost

        if self.live:
            self.live.update(self._generate_layout())

    def update_wave(self, wave_num: int, status: str, task_count: int = 0):
        """Update wave progress."""
        self.current_wave = wave_num
        self.wave_status[wave_num] = {
            "status": status,
            "task_count": task_count,
        }

        if self.live:
            self.live.update(self._generate_layout())

    def set_phase(self, phase_name: str):
        """Update current pipeline phase."""
        self.current_phase = phase_name
        if self.live:
            self.live.update(self._generate_layout())

    def add_cost(self, amount: float):
        """Increment running cost."""
        self.total_cost += amount
        if self.live:
            self.live.update(self._generate_layout())

    def log(self, message: str, style: str = ""):
        """Add log message below dashboard."""
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.logs.append(f"[dim]{timestamp}[/dim] {message}")
        # Keep last 5 logs
        if len(self.logs) > 5:
            self.logs.pop(0)

        if self.live:
            self.live.update(self._generate_layout())

    def _generate_layout(self):
        """Generate the full dashboard layout."""
        components = []

        # Header panel
        components.append(self._generate_header())

        # Progress bar
        components.append(self._generate_progress())

        # Task table
        if self.tasks:
            components.append(self._generate_task_table())

        # Logs
        if self.logs:
            components.append(self._generate_logs())

        return Group(*components)

    def _generate_header(self) -> Panel:
        """Generate header panel with run info."""
        elapsed = self._format_elapsed()
        done_tasks = sum(1 for t in self.tasks.values() if t["status"] == "pass")

        header = Table.grid(padding=(0, 2))
        header.add_column(justify="left")
        header.add_column(justify="right")

        header.add_row(
            f"[bold cyan]DISPATCH:[/bold cyan] {self.run_id}",
            f"[bold]Phase:[/bold] {self.current_phase}"
        )
        header.add_row(
            f"[bold]Wave[/bold] {self.current_wave}/{self.total_waves}  [bold]Tasks[/bold] {done_tasks}/{self.total_tasks}",
            f"[bold]Cost:[/bold] [green]${self.total_cost:.4f}[/green]  [bold]Elapsed:[/bold] {elapsed}"
        )

        return Panel(header, box=box.ROUNDED, border_style="cyan")

    def _generate_progress(self) -> Progress:
        """Generate progress bar."""
        done_tasks = sum(1 for t in self.tasks.values() if t["status"] == "pass")
        progress_pct = (done_tasks / self.total_tasks * 100) if self.total_tasks > 0 else 0

        progress = Progress(
            TextColumn("[progress.description]{task.description}"),
            BarColumn(bar_width=50),
            TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
            expand=False
        )

        task = progress.add_task("Progress", total=self.total_tasks, completed=done_tasks)
        return progress

    def _generate_task_table(self) -> Table:
        """Generate task status table."""
        table = Table(box=box.SIMPLE, show_header=True, header_style="bold")
        table.add_column("ID", width=6)
        table.add_column("Status", width=3)
        table.add_column("Description", min_width=30)
        table.add_column("Tokens", justify="right", width=8)
        table.add_column("Cost", justify="right", width=8)

        # Sort tasks by ID
        sorted_tasks = sorted(self.tasks.items(), key=lambda x: x[0])

        for task_id, task_info in sorted_tasks:
            status = task_info["status"]
            icon, color = STATUS_ICONS.get(status, ("?", "white"))

            # Add spinner for executing tasks
            if status == "executing":
                status_display = f"[{color}]{icon}[/{color}]"
            else:
                status_display = f"[{color}]{icon}[/{color}]"

            description = task_info.get("description", "")
            tokens = task_info.get("tokens", 0)
            cost = task_info.get("cost", 0.0)

            # Format tokens and cost
            tokens_str = f"{tokens:,}" if tokens > 0 else "..."
            cost_str = f"${cost:.3f}" if cost > 0 else "..."

            # Add error info if failed
            if status == "fail" and task_info.get("error"):
                description = f"{description} [red]({task_info['error']})[/red]"
            elif status == "retry":
                description = f"{description} [yellow](retrying)[/yellow]"

            table.add_row(
                task_id,
                status_display,
                description[:60] + "..." if len(description) > 60 else description,
                tokens_str,
                cost_str
            )

        return table

    def _generate_logs(self) -> Panel:
        """Generate logs panel."""
        log_text = "\n".join(self.logs)
        return Panel(log_text, title="[bold]Logs[/bold]", box=box.SIMPLE, border_style="dim")

    def _format_elapsed(self) -> str:
        """Format elapsed time."""
        if not self.start_time:
            return "00:00:00"

        elapsed = datetime.now() - self.start_time
        hours, remainder = divmod(int(elapsed.total_seconds()), 3600)
        minutes, seconds = divmod(remainder, 60)
        return f"{hours:02d}:{minutes:02d}:{seconds:02d}"


# Standalone functions for non-live contexts

def print_plan_summary(description: str, tasks: List[Dict], waves: List[List[str]],
                       models: Dict[str, str], cost_estimate: float):
    """Print plan summary with Rich formatting."""
    if not RICH_AVAILABLE:
        # Fallback to plain text
        print(f"\n{'='*60}")
        print(f"PLAN SUMMARY: {description}")
        print(f"{'='*60}")
        print(f"Tasks: {len(tasks)}")
        print(f"Waves: {len(waves)}")
        print(f"Estimated cost: ${cost_estimate:.4f}")
        print(f"{'='*60}\n")
        return

    console = Console()

    # Create summary table
    table = Table(box=box.ROUNDED, show_header=False, border_style="cyan")
    table.add_column(width=20, style="bold")
    table.add_column()

    table.add_row("Description", description)
    table.add_row("Total Tasks", str(len(tasks)))
    table.add_row("Total Waves", str(len(waves)))
    table.add_row("Estimated Cost", f"[green]${cost_estimate:.4f}[/green]")

    # Model distribution
    model_counts = {}
    for model in models.values():
        model_counts[model] = model_counts.get(model, 0) + 1

    model_str = ", ".join(f"{model}: {count}" for model, count in model_counts.items())
    table.add_row("Models", model_str)

    console.print(Panel(table, title="[bold cyan]DISPATCH PLAN[/bold cyan]", border_style="cyan"))


def print_wave_complete(wave_num: int, results: List[Dict], total_waves: int):
    """Print wave completion summary."""
    if not RICH_AVAILABLE:
        # Fallback
        print(f"\n--- Wave {wave_num}/{total_waves} Complete ---")
        passed = sum(1 for r in results if r.get("status") == "pass")
        print(f"Passed: {passed}/{len(results)}")
        print()
        return

    console = Console()

    passed = sum(1 for r in results if r.get("status") == "pass")
    failed = len(results) - passed

    # Wave summary
    table = Table(box=box.SIMPLE, show_header=True, header_style="bold")
    table.add_column("Task", width=10)
    table.add_column("Status", width=8)
    table.add_column("Tokens", justify="right", width=10)
    table.add_column("Cost", justify="right", width=10)

    total_tokens = 0
    total_cost = 0.0

    for result in results:
        task_id = result.get("task_id", "?")
        status = result.get("status", "unknown")
        tokens = result.get("tokens", 0)
        cost = result.get("cost", 0.0)

        total_tokens += tokens
        total_cost += cost

        icon, color = STATUS_ICONS.get(status, ("?", "white"))
        status_display = f"[{color}]{icon} {status}[/{color}]"

        table.add_row(
            task_id,
            status_display,
            f"{tokens:,}",
            f"${cost:.4f}"
        )

    # Add totals row
    table.add_row(
        "[bold]TOTAL[/bold]",
        f"[green]{passed}[/green]/[red]{failed}[/red]",
        f"[bold]{total_tokens:,}[/bold]",
        f"[bold green]${total_cost:.4f}[/bold green]"
    )

    title = f"[bold]Wave {wave_num}/{total_waves} Complete[/bold]"
    console.print(Panel(table, title=title, border_style="green" if failed == 0 else "yellow"))


def print_final_report(run_id: str, total_tasks: int, passed: int, failed: int,
                       cost: float, duration: float):
    """Print final execution report."""
    if not RICH_AVAILABLE:
        # Fallback
        print(f"\n{'='*60}")
        print(f"DISPATCH COMPLETE: {run_id}")
        print(f"{'='*60}")
        print(f"Tasks: {passed}/{total_tasks} passed, {failed} failed")
        print(f"Cost: ${cost:.4f}")
        print(f"Duration: {duration:.1f}s")
        print(f"{'='*60}\n")
        return

    console = Console()

    # Calculate metrics
    success_rate = (passed / total_tasks * 100) if total_tasks > 0 else 0
    cost_per_task = (cost / total_tasks) if total_tasks > 0 else 0

    # Format duration
    hours, remainder = divmod(int(duration), 3600)
    minutes, seconds = divmod(remainder, 60)
    duration_str = f"{hours:02d}:{minutes:02d}:{seconds:02d}"

    # Create report table
    table = Table(box=box.ROUNDED, show_header=False, border_style="cyan")
    table.add_column(width=20, style="bold")
    table.add_column()

    table.add_row("Run ID", run_id)
    table.add_row("Total Tasks", str(total_tasks))
    table.add_row("Passed", f"[green]{passed}[/green]")
    table.add_row("Failed", f"[red]{failed}[/red]" if failed > 0 else "0")
    table.add_row("Success Rate", f"{success_rate:.1f}%")
    table.add_row("Total Cost", f"[green]${cost:.4f}[/green]")
    table.add_row("Cost/Task", f"${cost_per_task:.4f}")
    table.add_row("Duration", duration_str)

    title = "[bold green]✅ DISPATCH COMPLETE[/bold green]" if failed == 0 else "[bold yellow]⚠️ DISPATCH COMPLETE (with errors)[/bold yellow]"
    console.print(Panel(table, title=title, border_style="green" if failed == 0 else "yellow"))


def print_cost_breakdown(by_model: Dict[str, Dict[str, float]]):
    """Print cost breakdown by model."""
    if not RICH_AVAILABLE:
        # Fallback
        print("\nCost Breakdown by Model:")
        for model, data in by_model.items():
            print(f"  {model}: ${data['cost']:.4f} ({data['tokens']:,} tokens)")
        print()
        return

    console = Console()

    # Create breakdown table
    table = Table(box=box.ROUNDED, show_header=True, header_style="bold")
    table.add_column("Model", width=20)
    table.add_column("Tasks", justify="right", width=10)
    table.add_column("Tokens", justify="right", width=15)
    table.add_column("Cost", justify="right", width=12)
    table.add_column("% of Total", justify="right", width=12)

    total_cost = sum(data["cost"] for data in by_model.values())
    total_tokens = sum(data["tokens"] for data in by_model.values())

    for model, data in sorted(by_model.items()):
        tasks = data.get("tasks", 0)
        tokens = data.get("tokens", 0)
        cost = data.get("cost", 0.0)
        pct = (cost / total_cost * 100) if total_cost > 0 else 0

        table.add_row(
            model,
            str(tasks),
            f"{tokens:,}",
            f"${cost:.4f}",
            f"{pct:.1f}%"
        )

    # Add totals
    table.add_row(
        "[bold]TOTAL[/bold]",
        "",
        f"[bold]{total_tokens:,}[/bold]",
        f"[bold green]${total_cost:.4f}[/bold green]",
        "[bold]100.0%[/bold]"
    )

    console.print(Panel(table, title="[bold]Cost Breakdown by Model[/bold]", border_style="cyan"))


def print_error(message: str):
    """Print error message with Rich formatting."""
    if not RICH_AVAILABLE:
        print(f"ERROR: {message}")
        return

    console = Console()
    console.print(f"[bold red]ERROR:[/bold red] {message}")


def print_warning(message: str):
    """Print warning message with Rich formatting."""
    if not RICH_AVAILABLE:
        print(f"WARNING: {message}")
        return

    console = Console()
    console.print(f"[bold yellow]WARNING:[/bold yellow] {message}")


def print_success(message: str):
    """Print success message with Rich formatting."""
    if not RICH_AVAILABLE:
        print(f"SUCCESS: {message}")
        return

    console = Console()
    console.print(f"[bold green]✅ SUCCESS:[/bold green] {message}")

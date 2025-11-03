import sys
from typing import Any, Callable, Dict, List, Optional

import typer
from pyfiglet import figlet_format
from rich import print as rprint
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt
from rich.table import Table
from rich.text import Text


class CLIWrapper:
    """
    A standardized CLI framework for horizon-core modules.
    Provides consistent interface, styling, and interactive features.
    """

    def __init__(
        self,
        app_name: str,
        app_description: str = "",
        version: str = "1.0.0",
        ascii_art: Optional[str] = None,
    ):
        self.app_name = app_name
        self.app_description = app_description
        self.version = version
        self.ascii_art = ascii_art

        # Initialize rich console
        self.console = Console()

        # Initialize typer app
        self.app = typer.Typer(
            name=app_name, help=app_description, add_completion=True, rich_markup_mode="rich"
        )

        # Add standard commands
        self._add_standard_commands()

        # Store interactive commands for help
        self.interactive_commands: Dict[str, Callable[[], Any]] = {}

    def _add_standard_commands(self):
        """Add standard CLI commands that all modules should have."""

        @self.app.command()
        def version():  # type: ignore
            """Show version information."""
            self._show_banner()
            rprint(
                f"[bold green]{self.app_name}[/bold green]"
                + f" version [bold blue]{self.version}[/bold blue]"
            )

        @self.app.command()
        def interactive():  # type: ignore
            """Launch interactive mode for guided usage."""
            self._interactive_mode()

    def _show_banner(self):
        """Display the application banner with ASCII art."""
        self.console.clear()

        if self.ascii_art:
            # Use custom ASCII art
            banner_text = self.ascii_art
        else:
            # Generate ASCII art from app name
            try:
                banner_text = figlet_format(self.app_name, font="big")
            except Exception:
                banner_text = f"=== {self.app_name.upper()} ==="

        # Create styled banner
        banner_panel = Panel(
            Text(banner_text, style="bold cyan"),
            title=f"[bold green]{self.app_description}[/bold green]",
            subtitle=f"[dim]v{self.version} - A HorizonSec Module[/dim]",
            border_style="blue",
        )

        self.console.print(banner_panel)
        self.console.print()

    def _interactive_mode(self):
        """Launch interactive mode with guided menu."""
        self._show_banner()

        while True:
            rprint("\n[bold cyan]Interactive Mode[/bold cyan]")
            rprint("What would you like to do?")

            # Build menu from registered commands
            choices = ["Show Help", "Exit"]
            for name in self.interactive_commands.keys():
                choices.insert(-1, name.title())

            table = Table(show_header=False, box=None)
            for i, choice in enumerate(choices, 1):
                table.add_row(f"[bold blue]{i}.[/bold blue]", choice)

            self.console.print(table)

            try:
                selection = Prompt.ask(
                    "\nEnter your choice",
                    choices=[str(i) for i in range(1, len(choices) + 1)],
                    default="1",
                )

                selection_idx = int(selection) - 1

                if choices[selection_idx] == "Exit":
                    rprint("[yellow]Goodbye! 👋[/yellow]")
                    break
                elif choices[selection_idx] == "Show Help":
                    self._show_interactive_help()
                else:
                    # Execute registered interactive command
                    cmd_name = choices[selection_idx].lower()
                    if cmd_name in self.interactive_commands:
                        self.interactive_commands[cmd_name]()

            except KeyboardInterrupt:
                rprint("\n[yellow]Goodbye! 👋[/yellow]")
                break
            except Exception as e:
                rprint(f"[red]Error: {e}[/red]")

    def _show_interactive_help(self):
        """Show help in interactive mode."""
        rprint("\n[bold green]Available Commands:[/bold green]")

        # Show typer commands
        commands_table = Table(title="CLI Commands")
        commands_table.add_column("Command", style="cyan")
        commands_table.add_column("Description", style="green")

        commands_table.add_row("--help", "Show detailed help")
        commands_table.add_row("version", "Show version information")
        commands_table.add_row("interactive", "Launch this interactive mode")

        self.console.print(commands_table)

        if self.interactive_commands:
            rprint("\n[bold green]Interactive Features:[/bold green]")
            for name, func in self.interactive_commands.items():
                doc = func.__doc__ or "No description available"
                rprint(f"• [cyan]{name.title()}[/cyan]: {doc}")

    def register_interactive_command(self, name: str, func: Callable[[], Any]):
        """Register a custom interactive command."""
        self.interactive_commands[name] = func

    def add_command(self, func: Callable[..., Any]):
        """Add a custom command to the CLI."""
        return self.app.command()(func)

    def add_group(self, name: str, help: str = "") -> typer.Typer:
        """Add a command group."""
        group = typer.Typer(name=name, help=help)
        self.app.add_typer(group, name=name)
        return group

    def run(self, args: Optional[List[str]] = None):
        """Run the CLI application."""
        self._show_banner()
        if args is None:
            args = sys.argv[1:]

        # If no arguments provided, show banner and help
        if not args:
            rprint(
                "[dim]Use --help for available commands or 'interactive' for guided mode[/dim]\n"
            )

        try:
            self.app()
        except KeyboardInterrupt:
            rprint("\n[yellow]Operation cancelled[/yellow]")
            sys.exit(1)
        except Exception as e:
            rprint(f"[red]Error: {e}[/red]")
            sys.exit(1)


# Utility function for easy CLI creation


def create_cli(
    app_name: str,
    app_description: str = "",
    version: str = "1.0.0",
    ascii_art: Optional[str] = None,
) -> CLIWrapper:
    """
    Factory function to create a CLI framework instance.

    Args:
        app_name: Name of the application
        app_description: Brief description of the application
        version: Application version
        ascii_art: Custom ASCII art for banner (optional)

    Returns:
        CLI instance ready for use
    """
    return CLIWrapper(
        app_name=app_name, app_description=app_description, version=version, ascii_art=ascii_art
    )

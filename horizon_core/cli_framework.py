"""
CLI Framework - Standardized command-line interface utilities.

This module provides a base framework for building consistent CLI tools
across the HorizonSec ecosystem.
"""

import argparse
import sys
from abc import ABC, abstractmethod
from typing import List, Optional


class Command(ABC):
    """Base class for CLI commands."""

    def __init__(self, name: str, description: str):
        """
        Initialize a command.

        Args:
            name: The command name
            description: A brief description of what the command does
        """
        self.name = name
        self.description = description

    @abstractmethod
    def configure_parser(self, parser: argparse.ArgumentParser) -> None:
        """
        Configure the argument parser for this command.

        Args:
            parser: The argument parser to configure
        """
        pass

    @abstractmethod
    def execute(self, args: argparse.Namespace) -> int:
        """
        Execute the command.

        Args:
            args: Parsed command-line arguments

        Returns:
            Exit code (0 for success, non-zero for failure)
        """
        pass


class CLI:
    """Main CLI application class."""

    def __init__(self, name: str, description: str, version: str):
        """
        Initialize the CLI application.

        Args:
            name: Application name
            description: Application description
            version: Application version
        """
        self.name = name
        self.description = description
        self.version = version
        self.commands: List[Command] = []
        self.parser = argparse.ArgumentParser(
            prog=name,
            description=description,
            formatter_class=argparse.RawDescriptionHelpFormatter,
        )
        self.parser.add_argument(
            "--version",
            action="version",
            version=f"{name} {version}",
        )

    def add_command(self, command: Command) -> None:
        """
        Add a command to the CLI.

        Args:
            command: The command to add
        """
        self.commands.append(command)

    def run(self, argv: Optional[List[str]] = None) -> int:
        """
        Run the CLI application.

        Args:
            argv: Command-line arguments (defaults to sys.argv[1:])

        Returns:
            Exit code
        """
        if not self.commands:
            self.parser.print_help()
            return 1

        # Create subparsers for commands
        subparsers = self.parser.add_subparsers(
            title="commands",
            dest="command",
            help="Available commands",
        )

        # Register all commands
        command_map = {}
        for command in self.commands:
            cmd_parser = subparsers.add_parser(
                command.name,
                help=command.description,
            )
            command.configure_parser(cmd_parser)
            command_map[command.name] = command

        # Parse arguments
        args = self.parser.parse_args(argv)

        # Execute the selected command
        if not args.command:
            self.parser.print_help()
            return 1

        command = command_map[args.command]
        try:
            return command.execute(args)
        except Exception as e:
            print(f"Error executing command '{args.command}': {e}", file=sys.stderr)
            return 1

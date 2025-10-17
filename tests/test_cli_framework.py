"""Tests for CLI framework."""

import argparse
from horizon_core.cli_framework import CLI, Command


class DummyCommand(Command):
    """A dummy command for testing."""

    def __init__(self):
        super().__init__("test", "A test command")
        self.executed = False
        self.args = None

    def configure_parser(self, parser: argparse.ArgumentParser) -> None:
        parser.add_argument("--option", help="A test option")

    def execute(self, args: argparse.Namespace) -> int:
        self.executed = True
        self.args = args
        return 0


def test_cli_creation():
    """Test CLI creation."""
    cli = CLI("test-cli", "Test CLI", "1.0.0")
    assert cli.name == "test-cli"
    assert cli.description == "Test CLI"
    assert cli.version == "1.0.0"


def test_add_command():
    """Test adding a command to CLI."""
    cli = CLI("test-cli", "Test CLI", "1.0.0")
    cmd = DummyCommand()
    cli.add_command(cmd)
    assert len(cli.commands) == 1
    assert cli.commands[0] == cmd


def test_command_execution():
    """Test command execution."""
    cli = CLI("test-cli", "Test CLI", "1.0.0")
    cmd = DummyCommand()
    cli.add_command(cmd)

    result = cli.run(["test", "--option", "value"])
    assert result == 0
    assert cmd.executed is True
    assert cmd.args.option == "value"


def test_cli_no_command():
    """Test CLI with no command specified."""
    cli = CLI("test-cli", "Test CLI", "1.0.0")
    cmd = DummyCommand()
    cli.add_command(cmd)

    result = cli.run([])
    assert result == 1
    assert cmd.executed is False

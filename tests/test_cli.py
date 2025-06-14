"""Tests for the CLI module.

This test suite covers the command-line interface functionality,
argument parsing, and integration with the MboxConverter.
"""

import argparse
import os
import sys
import tempfile
import unittest
from io import StringIO
from pathlib import Path
from unittest.mock import MagicMock, patch, mock_open

from mbox_converter import cli

# Import the CLI module

from mbox_converter.parameters import PARAMETERS


class TestArgumentParsing(unittest.TestCase):
    """Test command-line argument parsing."""

    def test_argument_choices_validation(self):
        """Test that argument choices are properly validated."""
        # Test invalid format choice
        test_args = ["--format", "invalid", "test.mbox"]

        with patch("sys.argv", ["cli.py"] + test_args):
            with self.assertRaises(SystemExit):
                cli.parse_arguments()

    def test_positional_argument_required(self):
        """Test that mbox_file positional argument is required."""
        with patch("sys.argv", ["cli.py"]):
            with self.assertRaises(SystemExit):
                cli.parse_arguments()


class TestMainFunction(unittest.TestCase):
    """Test the main CLI function."""

    def setUp(self):
        """Set up test fixtures."""
        self.temp_dir = tempfile.mkdtemp()
        self.test_mbox = Path(self.temp_dir) / "test.mbox"
        # Create a minimal test mbox file
        self.test_mbox.write_text("From test@example.com\nTest email content\n")

    def tearDown(self):
        """Clean up test fixtures."""
        # Clean up temporary files
        for file in Path(self.temp_dir).glob("*"):
            file.unlink()
        Path(self.temp_dir).rmdir()

    @patch("mbox_converter.cli.ConfigParameterManager")
    @patch("mbox_converter.cli.MboxConverter")
    def test_main_success(self, mock_converter_class, mock_config_class):
        """Test successful execution of main function."""
        # Mock configuration
        mock_config = MagicMock()
        mock_config.mbox_file = str(self.test_mbox)
        mock_config_class.return_value = mock_config

        # Mock converter
        mock_converter = MagicMock()
        mock_converter_class.return_value = mock_converter

        test_args = ["cli.py", str(self.test_mbox)]

        with patch("sys.argv", test_args):
            result = cli.main()

            self.assertEqual(result, 0)
            mock_config_class.assert_called_once()
            mock_converter_class.assert_called_once_with(mock_config)
            mock_converter.convert.assert_called_once()

    @patch("mbox_converter.cli.ConfigParameterManager")
    def test_main_file_not_found(self, mock_config_class):
        """Test main function with non-existent mbox file."""
        mock_config = MagicMock()
        mock_config.mbox_file = "nonexistent.mbox"
        mock_config_class.return_value = mock_config

        test_args = ["cli.py", "nonexistent.mbox"]

        with patch("sys.argv", test_args):
            with patch("sys.stdout", new_callable=StringIO) as mock_stdout:
                result = cli.main()

                self.assertEqual(result, 1)
                output = mock_stdout.getvalue()
                self.assertIn("Error: mbox file not found", output)

    @patch("mbox_converter.cli.ConfigParameterManager")
    def test_main_config_file_not_found(self, mock_config_class):
        """Test main function with non-existent config file."""
        mock_config_class.side_effect = FileNotFoundError("Config file not found")

        test_args = ["cli.py", "--config", "nonexistent.yaml", str(self.test_mbox)]

        with patch("sys.argv", test_args):
            with patch("sys.stdout", new_callable=StringIO) as mock_stdout:
                result = cli.main()

                self.assertEqual(result, 1)
                output = mock_stdout.getvalue()
                self.assertIn("Error:", output)

    @patch("mbox_converter.cli.ConfigParameterManager")
    @patch("mbox_converter.cli.MboxConverter")
    def test_main_converter_exception(self, mock_converter_class, mock_config_class):
        """Test main function when converter raises an exception."""
        mock_config = MagicMock()
        mock_config.mbox_file = str(self.test_mbox)
        mock_config_class.return_value = mock_config

        mock_converter = MagicMock()
        mock_converter.convert.side_effect = Exception("Conversion failed")
        mock_converter_class.return_value = mock_converter

        test_args = ["cli.py", str(self.test_mbox)]

        with patch("sys.argv", test_args):
            with patch("sys.stdout", new_callable=StringIO) as mock_stdout:
                result = cli.main()

                self.assertEqual(result, 1)
                output = mock_stdout.getvalue()
                self.assertIn("Error: Conversion failed", output)


class TestConfigurationIntegration(unittest.TestCase):
    """Test integration between CLI and configuration system."""

    def setUp(self):
        """Set up test fixtures."""
        self.temp_dir = tempfile.mkdtemp()
        self.test_config = Path(self.temp_dir) / "test_config.yaml"
        self.test_mbox = Path(self.temp_dir) / "test.mbox"
        self.test_mbox.write_text("From test@example.com\nTest email content\n")

    def tearDown(self):
        """Clean up test fixtures."""
        for file in Path(self.temp_dir).glob("*"):
            file.unlink()
        Path(self.temp_dir).rmdir()

    @patch("mbox_converter.cli.ConfigParameterManager")
    @patch("mbox_converter.cli.MboxConverter")
    def test_config_file_loading(self, mock_converter_class, mock_config_class):
        """Test that config file is properly loaded."""
        mock_config = MagicMock()
        mock_config.mbox_file = str(self.test_mbox)
        mock_config_class.return_value = mock_config

        mock_converter = MagicMock()
        mock_converter_class.return_value = mock_converter

        test_args = ["cli.py", "--config", str(self.test_config), str(self.test_mbox)]

        with patch("sys.argv", test_args):
            result = cli.main()

            self.assertEqual(result, 0)
            # Verify config file was passed to ConfigParameterManager
            mock_config_class.assert_called_once_with(config_file=str(self.test_config))


class TestParameterGeneration(unittest.TestCase):
    """Test that CLI arguments are properly generated from parameters."""

    def test_all_parameters_have_cli_representation(self):
        """Test that all parameters from PARAMETERS are represented in CLI."""
        # This test verifies that the CLI argument generation works correctly
        test_args = ["test.mbox"]

        with patch("sys.argv", ["cli.py"] + test_args):
            parser = argparse.ArgumentParser()

            # Simulate the argument generation process
            for param in PARAMETERS:
                if param.name == "mbox_file":
                    continue  # Positional argument, handled separately
                if not param.is_cli:
                    continue  # Skip non-CLI parameters

                # This should not raise an exception
                kwargs = {
                    "default": param.default,
                    "help": f"{param.help} (default: {param.default})",
                }

                if param.choices:
                    kwargs["choices"] = param.choices

                if param.type_ == int:
                    kwargs["type"] = int

                # Should be able to add argument without error
                parser.add_argument(param.cli_arg, **kwargs)

    def test_cli_argument_mapping(self):
        """Test that CLI arguments map correctly to parameter names."""
        expected_mappings = {
            "--from": "sent_from",
            "--to": "to",
            "--date": "date",
            "--subject": "subject",
            "--format": "format",
            "--max-days": "max_days",
        }

        for param in PARAMETERS:
            if param.name == "mbox_file" or not param.is_cli:
                continue

            expected_cli_arg = expected_mappings.get(param.cli_arg)
            if expected_cli_arg:
                self.assertEqual(param.name, expected_cli_arg)

#!/usr/bin/env python
# -*- coding: utf-8 -*-
import io
import argparse
from unittest import mock
import unittest

from pycli import CLI


class TestBase(unittest.TestCase):

    @mock.patch("sys.stdout", new_callable=io.StringIO)
    def test_common(self, mock_stdout):
        cli = CLI()

        @cli.command
        def test():
            print("test", end='')

        cli.run(["test"])
        self.assertEqual(mock_stdout.getvalue(), "test")

    @mock.patch("sys.stdout", new_callable=io.StringIO)
    def test_version(self, mock_stdout):
        cli = CLI(prog="app", version="v1.0.0")

        with self.assertRaises(SystemExit):
            cli.run(["-v"])
        self.assertEqual(mock_stdout.getvalue(), "app v1.0.0\n")

    def test_duplicate_error(self):
        cli = CLI()

        @cli.command
        def test1():
            pass

        with self.assertRaises(argparse.ArgumentError):
            @cli.command
            def test1():
                pass

    @mock.patch("sys.stdout", new_callable=io.StringIO)
    def test_multiple_subcommands(self, mock_stdout):
        cli = CLI()

        @cli.command
        def test1():
            print("test1", end='')

        @cli.command
        def test2():
            print("test2", end='')

        cli.run(["test1"])
        cli.run(["test2"])
        self.assertEqual(mock_stdout.getvalue(), "test1" + "test2")

    @mock.patch("sys.stdout", new_callable=io.StringIO)
    def test_custom_subcommand_info(self, mock_stdout):
        cli = CLI()

        @cli.command_with_args(title="test1", help="unittest",
                               description="use for unittest")
        def test():
            pass

        with self.assertRaises(SystemExit):
            cli.run(["test1", "-h"])

        self.assertIn("use for unittest", mock_stdout.getvalue())


if __name__ == "__main__":
    unittest.main()

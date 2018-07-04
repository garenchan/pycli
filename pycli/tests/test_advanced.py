#!/usr/bin/env python
# -*- coding: utf-8 -*-
import unittest

from pycli import CLI


class TestAdvanced(unittest.TestCase):

    def test_arguments(self):
        cli = CLI()

        @cli.command
        def add(a, b):
            return a + b

        ret = cli.run(["add", "1", "2"])
        self.assertEqual(ret, "12")

    def test_annotation(self):
        cli = CLI()

        @cli.command
        def add(a: int, b: int):
            return a + b

        ret = cli.run(["add", "1", "2"])
        self.assertEqual(ret, 3)

    def test_argument_default(self):
        cli = CLI()

        @cli.command
        def add(a: int, b: int = 3):
            return a + b

        ret = cli.run(["add", "1"])
        self.assertEqual(ret, 4)

    def test_multiple_argument(self):
        cli = CLI()

        @cli.command
        def multi(a, b: list):
            return b

        ret = cli.run(["multi", "", "--b", "1", "--b", "2"])
        self.assertEqual(ret, ["1", "2"])

    def test_bool_argument(self):
        cli = CLI()

        @cli.command
        def close(switch: bool = True):
            return switch

        ret = cli.run(["close", "--switch"])
        self.assertIs(ret, False)

    def test_argparse_compatible(self):
        cli = CLI()

        cli.add_argument("-a", action="store", default=1)
        cli.add_argument("-b", action="store_true", default=False)

        namespace = cli.parse_args(["-b"])
        self.assertEqual(namespace.b, True)


if __name__ == '__main__':
    unittest.main()

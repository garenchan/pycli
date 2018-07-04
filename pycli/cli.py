#!/usr/bin/env python
# -*- coding: utf-8 -*-
import collections
import inspect
import argparse


class CLI(argparse.ArgumentParser):
    """A CLI Based On argparse
    """

    # Don't used this string as an argument name
    SUBCOMMAND_MAGIC_FUNC = "__SUBCOMMAND_MAGIC_FUNC__"

    def __init__(self,
                 prog=None,
                 version=None,
                 usage=None,
                 description=None,
                 epilog=None,
                 prefix_chars='-',
                 fromfile_prefix_chars=None,
                 conflict_handler="error",
                 add_help=True,
                 group_name="subcommands"):
        super().__init__(
            prog=prog,
            usage=usage,
            description=description,
            epilog=epilog,
            formatter_class=argparse.ArgumentDefaultsHelpFormatter,
            prefix_chars=prefix_chars,
            fromfile_prefix_chars=fromfile_prefix_chars,
            conflict_handler=conflict_handler,
            add_help=add_help,
        )
        self.group_name = group_name
        if version:
            self.add_argument(
                "-v", "--version",
                action="version",
                version="%(prog)s {}".format(version))

    def command_with_args(self, title=None, help=None, description=None):
        """A decorator for subcommand function
        :param title: subcommand name
        :param help: subcommand help
        :param description: subcommand description
        :return:
        """

        def wrapper(_callable):
            assert callable(_callable)
            nonlocal title, help, description

            if not getattr(self, "subparser", None):
                self.subparser = self.add_subparsers(title=self.group_name)

            if not title:
                try:
                    title = _callable.__name__
                except AttributeError:
                    title = _callable.__class__.__name__
            if not description:
                description = _callable.__doc__
            if self.subparser.choices.get(title):
                message = "SubCommand %r Already Exists" % title
                raise argparse.ArgumentError(None, message)
            _parser = self.subparser.add_parser(title,
                                                help=help,
                                                description=description)
            _parser.set_defaults(**{self.SUBCOMMAND_MAGIC_FUNC: _callable})

            fullargspec = inspect.getfullargspec(_callable)
            # NOTE: argument maybe has default value of None,
            # so we use a sentinel to judge whether it has default value.
            _sentinel = object()

            def add_subcommand_arguments(arg, default, annotation):
                action_name = "store"
                if annotation:
                    if annotation not in [bytes, str] and \
                            issubclass(annotation, collections.Iterable):
                        action_name = "append"
                    elif annotation is bool:
                        if default is _sentinel or not isinstance(default, bool):
                            message = "bool argument must has a default value"
                            raise argparse.ArgumentError(None, message)
                        action_name = "store_false" if default else "store_true"
                # NOTE: if argument has default value or append action,
                # make it optional.
                name = self.prefix_chars[0] * 2 + arg.replace('_', '-') \
                    if default is not _sentinel or action_name == "append" \
                    else arg

                action = _parser.add_argument(name, action=action_name)

                if default is not _sentinel:
                    action.default = default
                    # force the default value display while print help
                    action.help = " "
                    action.required = False
                else:
                    action.required = True
                if annotation:
                    if annotation in [bytes, str] or \
                            not issubclass(annotation, collections.Iterable):
                        action.type = annotation
                        action.help = "type: <%s>" % annotation.__name__
                    elif annotation not in [bytes, str] and \
                            issubclass(annotation, collections.Iterable):
                        action.help = "type: <multi>"

            for index, arg in enumerate(fullargspec.args,
                                        len(fullargspec.args) * -1):
                annotation = fullargspec.annotations.get(arg)
                default = fullargspec.defaults[index] \
                    if fullargspec.defaults and \
                    len(fullargspec.defaults) >= abs(index) else _sentinel
                add_subcommand_arguments(arg, default, annotation)

            for kwarg in fullargspec.kwonlyargs:
                annotation = fullargspec.annotations.get(kwarg)
                default = fullargspec.kwonlydefaults.get(kwarg, _sentinel)
                add_subcommand_arguments(kwarg, default, annotation)

            return _callable

        return wrapper

    def command(self, _callable):
        """A decorator for subcommand function with default title and
           empty description
        :param _callable: a callable object, such as function
        :return:
        """
        wrapper = self.command_with_args()
        return wrapper(_callable)

    def run(self, args=None):
        namespace = self.parse_args(args)
        args = namespace.__dict__
        callback = args.pop(self.SUBCOMMAND_MAGIC_FUNC, None)
        if callback:
            return callback(**args)

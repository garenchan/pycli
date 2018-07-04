# PyCLI
A Tiny Python CLI Library Based On `argparse`, make it easier for us to add subcommands.

If you use argparse to parse arguments, and you are very upset about adding subcommands and their handlers, then PyCLI is what you want.

[![Build Status](https://api.travis-ci.org/garenchan/pycli.svg?branch=master)](https://travis-ci.org/garenchan/pycli)

## Demo

Here is the simplest demo for pycli.

```
# demo.py
from pycli import CLI

cli = CLI(prog="app", version="v1.0.0")

@cli.command
def add(x, y):
    """get sum of two numbers"""
    return x + y

print(cli.run())
```

Then we run it to get help information, a subcommand named `add` is added:
```
$ python demo.py -h
usage: app [-h] [-v] {add} ...

optional arguments:
  -h, --help     show this help message and exit
  -v, --version  show program's version number and exit

subcommands:
  {add}
```

Next we lookup the help information of the subcommand, two positional arguments are added:
```
$ python demo.py add -h
usage: app add [-h] x y

get sum of two numbers

positional arguments:
  x
  y

optional arguments:
  -h, --help  show this help message and exit
```

We use the subcommand to get sum of two numbers, the output we expected is 3, but 12 is given, so we need to specify the type of arguments:
```
$ python demo.py add 1 2
12
```

## Argument Type

By default, type of arguments is `str`, we can change it by function annotation.

We specify argument `x` and `y` of type int:

```
# demo.py
from pycli import CLI

cli = CLI(prog="app", version="v1.0.0")

@cli.command
def add(x: int, y: int):
    """get sum of two numbers"""
    return x + y

print(cli.run())
```

We run the subcommand to get sum of 1 and 2, now result 3 is given:

```
# python demo.py add 1 2
3
```

## Default Argument

Some arguments may have default values, so we can make it optional and no need to pass them while run.

```
# demo.py
from pycli import CLI

cli = CLI(prog="app", version="v1.0.0")

@cli.command
def add(x: int, y: int = 3):
    """get sum of two numbers"""
    return x + y

print(cli.run())
```

We lookup the help information of the subcommand, `y` becomes a optional argument:

```
$ python demo.py add -h
usage: app add [-h] [--y Y] x

get sum of two numbers

positional arguments:
  x           type: <int>

optional arguments:
  -h, --help  show this help message and exit
  --y Y       type: <int> (default: 3)
```

## List Argument

Sometimes we may need a list argument, for example, specifying multiple configuration files:

```
# demo.py
from pycli import CLI

cli = CLI(prog="app", version="v1.0.0")

@cli.command
def init(conf_files: list):
    """Initialize system"""

    # do something here
    return conf_files

print(cli.run())
```

Now we can pass multiple values to the same argument, and a list of string will return:

```
$ python demo.py init --conf-files a.ini --conf-files b.ini
['a.ini', 'b.ini']
```

## Bool Argument

Sometimes we need a argument as a switch, we can speficy its type as bool and give it a default value True/False.

If we pass it when run, its value will be switched:

```
# demo.py
import queue
from pycli import CLI

cli = CLI(prog="app", version="v1.0.0")
q = queue.Queue()

@cli.command
def get(block: bool = True):
    """get a item"""

    return q.get(block)

print(cli.run())
```

## Custom Subcommand

By default, PyCLI use function name or object's class name as subcommand title, and use docstring as subcommand description.

You can custom them as you wish:

```
# demo.py
from pycli import CLI

cli = CLI(prog="app", version="v1.0.0")

@cli.command_with_args(title="sum", description="Sum of two integers")
def add(x: int, y: int):
    """get sum of two numbers"""
    return x + y

print(cli.run())
```

Now a subcommand named `sum` is added as follow:

```
$ python demo.py sum -h
usage: app sum [-h] x y

Sum of two integers

positional arguments:
  x           type: <int>
  y           type: <int>

optional arguments:
  -h, --help  show this help message and exit
```

## Integration With Argparse

`pycli.CLI` is a subclass of `argparse.ArgumentParser`, so it has some APIs as `ArgumentParser`.

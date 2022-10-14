# -*- coding: utf-8 -*-

"""
Package xxd
=======================================

Top-level package for xxd.
"""

__version__ = "0.0.0"

try:
    import xxd.morton
except ModuleNotFoundError as e:
    # Try to build this binary extension:
    from pathlib import Path
    import click
    from et_micc2.project import auto_build_binary_extension
    msg = auto_build_binary_extension(Path(__file__).parent, 'morton')
    if not msg:
        import xxd.morton
    else:
        click.secho(msg, fg='bright_red')


def hello(who='world'):
    """'Hello world' method.

    :param str who: whom to say hello to
    :returns: a string
    """
    result = "Hello " + who
    return result

# Your code here...
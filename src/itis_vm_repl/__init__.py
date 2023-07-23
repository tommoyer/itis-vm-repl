# SPDX-FileCopyrightText: 2023-present Tom Moyer <tom.moyer@uncc.edu>
#
# SPDX-License-Identifier: MIT
import click

from click_repl import repl
from prompt_toolkit.history import FileHistory
from .interactive_command import interactive_command
from importlib_metadata import version

__version__ = version(__package__)


@click.group(context_settings={"help_option_names": ["-h", "--help"]}, invoke_without_command=True)
@click.version_option(version=__version__, prog_name="ITIS VM REPL")
def itis_vm_repl():
    pass


@itis_vm_repl.command()
def test():
    interactive_command('/bin/bash')


@itis_vm_repl.command()
def vmrepl():
    click.echo("Use ':quit' or Ctrl+D to quit.")
    prompt_kwargs = {
        'history': FileHistory('/tmp/repl-history'),
    }
    repl(click.get_current_context(), prompt_kwargs=prompt_kwargs)


if __name__ == '__main__':
    itis_vm_repl()

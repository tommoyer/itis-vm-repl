# SPDX-FileCopyrightText: 2023-present Tom Moyer <tom.moyer@uncc.edu>
#
# SPDX-License-Identifier: MIT

from rich import print
from typer import Context

from typer_shell import make_typer_shell


class App:
    def __init__(self):
        pass


app = make_typer_shell(prompt="💻: ", obj=App(), intro='\n Welcome to the ITIS VM shell\n Type help to see commands\n Type quit or exit to leave\n')
app._add_completion = False


@app.command()
def foobar():
    '''
    Foobar command
    '''
    print('Called foobar')


@app.command()
def name(ctx: Context):
    '''
    Name command
    '''
    print('Called name command')


if __name__ == "__main__":
    app()

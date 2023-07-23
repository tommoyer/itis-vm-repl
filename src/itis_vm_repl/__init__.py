# SPDX-FileCopyrightText: 2023-present Tom Moyer <tom.moyer@uncc.edu>
#
# SPDX-License-Identifier: MIT

from rich import print
from typer import Context, Argument, Option

from typer_shell import make_typer_shell
from typing_extensions import Annotated

intro_help = '''
 Welcome to the ITIS VM shell
 Type help to see commands
 Type help <COMMAND> to see detailed help for a specific command
 Type quit or exit to leave
'''


class App:
    def __init__(self):
        pass


app = make_typer_shell(prompt="💻: ", obj=App(), intro=intro_help)
app._add_completion = False


@app.command(hidden=True)
def lxd_init(ctx: Context):
    '''
    Initialize LXD
    '''
    print('Called lxd-init')


@app.command()
def create(ctx: Context):
    '''
    Create new container
    '''
    print('Called create command')


@app.command()
def shell(ctx: Context,
          container_name: Annotated[str, Argument(help="The name of the container", show_default=False)],
          root: Annotated[bool, Option("--root", help="Login as root user")] = False):
    '''
    Access the shell for CONTAINER
    '''
    print(f'Called shell command for {container_name}')


@app.command()
def start(ctx: Context,
          container_name: Annotated[str, Argument(help="The name of the container", show_default=False)]):
    '''
    Start the container CONTAINER
    '''
    print(f'Called start command for {container_name}')


@app.command()
def stop(ctx: Context,
         container_name: Annotated[str, Argument(help="The name of the container", show_default=False)]):
    '''
    Stop the container CONTAINER
    '''
    print(f'Called stop command for {container_name}')


@app.command()
def restart(ctx: Context,
            container_name: Annotated[str, Argument(help="The name of the container", show_default=False)]):
    '''
    Restart the container CONTAINER
    '''
    print(f'Called restart command for {container_name}')


@app.command()
def pull_file(ctx: Context,
              container_name: Annotated[str, Argument(help="The name of the container", show_default=False)],
              file: Annotated[str, Argument(help="The full path of the file inside the container", show_default=False)]):
    '''
    Pull a file FILE from the container CONTAINER
    '''
    print(f'Called pull {file} command from {container_name}')


@app.command()
def push_file(ctx: Context,
              container_name: Annotated[str, Argument(help="The name of the container", show_default=False)],
              file: Annotated[str, Argument(help="The full path of the file inside the container", show_default=False)]):
    '''
    Push a file FILE into the container CONTAINER
    '''
    print(f'Called push {file} command into {container_name}')


@app.command()
def create_proxy_port(ctx: Context,
                      container_name: Annotated[str, Argument(help="The name of the container", show_default=False)],
                      container_port: Annotated[int, Argument(help="The port on the container to connect to", show_default=False)],
                      vm_port: Annotated[int, Argument(help="The port on the VM to listen on", show_default=False)]):
    '''
    Setup a proxy port from the VM port number VM_PORT to CONTAINER_PORT on the container CONTAINER_NAME
    '''
    print(f'Called proxy-port command {container_name}:{container_port} to port {vm_port} on the VM')


@app.command()
def delete_proxy_port(ctx: Context,
                      container_name: Annotated[str, Argument(help="The name of the container", show_default=False)],
                      container_port: Annotated[int, Argument(help="The port on the container to connect to", show_default=False)]):
    '''
    Delete a proxy port from the CONTAINER_PORT on the container CONTAINER_NAME
    '''
    print(f'Called delete-proxy-port command {container_name}:{container_port}')


if __name__ == "__main__":
    app()

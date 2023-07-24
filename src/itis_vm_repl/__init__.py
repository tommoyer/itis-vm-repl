# SPDX-FileCopyrightText: 2023-present Tom Moyer <tom.moyer@uncc.edu>
#
# SPDX-License-Identifier: MIT

import subprocess

from rich import print
from rich.console import Console
from typer import Context, Argument, Option, confirm
from typer_shell import make_typer_shell
from typing_extensions import Annotated
from .interactive_command import interactive_command
from dataclasses import dataclass


intro_help = '''
 Welcome to the ITIS VM shell
 Type help to see commands
 Type help <COMMAND> to see detailed help for a specific command
 Type quit or exit to leave
'''

console = Console(color_system=None)


class App:
    def __init__(self):
        pass


@dataclass
class State:
    ''' Class for state tracking '''
    verbose: bool = False
    debug: bool = False

    def toggle_debug(self):
        self.debug = not self.debug
        print(f'Debug set to: {state.debug}')

    def toggle_verbose(self):
        self.verbose = not self.verbose
        print(f'Verbose set to: {state.verbose}')


app = make_typer_shell(prompt="💻: ", obj=App(), intro=intro_help)
app._add_completion = False
state = State()


@app.command(hidden=True)
def lxd_init(ctx: Context):
    '''
    Initialize LXD
    '''
    print('Called lxd-init')


@app.command(hidden=True)
def vm_shell(ctx: Context):
    '''
    Access shell on VM
    '''
    interactive_command(['/bin/bash', '-l'])


@app.command(hidden=True)
def verbose(ctx: Context):
    '''
    Toggle the verbosity
    '''
    state.toggle_verbose()


@app.command(hidden=True)
def debug(ctx: Context):
    '''
    Toggle debug output
    '''
    state.toggle_debug()


@app.command()
def list(ctx: Context):
    '''
    List containers
    '''
    command = ['/snap/bin/lxc', 'list']
    output = subprocess.run(command, capture_output=True)
    console.print(output.stdout.decode('utf-8'))


@app.command()
def reboot(ctx: Context):
    '''
    Reboot the VM
    '''
    if confirm('Are you sure you want to reboot?'):
        if state.debug:
            print('Rebooting the VM now')
        else:
            subprocess.run(['sudo', 'shutdown', '-r', 'now'])


@app.command()
def shutdown(ctx: Context):
    '''
    Shutdown the VM
    '''
    if confirm('Are you sure you want to shutdown?'):
        if state.debug:
            print('Shutting down the VM now')
        else:
            subprocess.run(['sudo', 'shutdown', '-h', 'now'])


@app.command()
def create(ctx: Context,
           container_name: Annotated[str, Argument(help="The name of the container", show_default=False)],
           ip_address: Annotated[str, Argument(help="The IP address of the container", show_default=False)],):
    '''
    Create new container
    '''
    print('Called create')


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

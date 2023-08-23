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
from pathlib import Path


intro_help = '''
 Welcome to the ITIS VM shell
 Type help to see commands
 Type help <COMMAND> to see detailed help for a specific command
 Type quit or exit to leave
'''

console = Console(color_system=None)
store_path = Path('/home/ubuntu/files/')


class App:
    def __init__(self):
        pass


@dataclass
class State:
    ''' Class for state tracking '''
    debug: bool = False
    fake: bool = False

    def toggle_debug(self):
        self.debug = not self.debug
        print(f'Debug set to: {state.debug}')

    def toggle_fake(self):
        self.fake = not self.fake
        print(f'Fake set to: {state.fake}')


app = make_typer_shell(prompt="💻: ", obj=App(), intro=intro_help)
app._add_completion = False
state = State()


def non_interactive_command(command: list[str]):
    if state.debug or state.fake:
        print('Running command:')
        print(' '.join(command))
    if not state.fake:
        output = subprocess.run(command, capture_output=True)
        if len(output.stdout.decode('utf-8')) > 0:
            console.print(output.stdout.decode('utf-8'))


def ensure_file_store():
    store_path.mkdir(parents=True, exist_ok=True)


@app.command(hidden=True)
def lxd_init(ctx: Context):
    '''
    Initialize LXD
    '''
    interactive_command(['/snap/bin/lxd', 'init'], state.fake)


@app.command(hidden=True)
def _vm_shell(ctx: Context):
    '''
    Access shell on VM
    '''
    interactive_command(['/bin/bash', '-l'], state.fake)


@app.command(hidden=True)
def _debug(ctx: Context):
    '''
    Toggle debug output
    '''
    state.toggle_debug()


@app.command(hidden=True)
def _fake(ctx: Context):
    '''
    Toggle fake operation
    '''
    state.toggle_fake()


@app.command()
def list(ctx: Context):
    '''
    List containers
    '''
    non_interactive_command(['/snap/bin/lxc', 'list'])


@app.command()
def reboot(ctx: Context):
    '''
    Reboot the VM
    '''
    if confirm('Are you sure you want to reboot?'):
        if state.fake:
            print('Fake: rebooting the VM now')
        else:
            subprocess.run(['sudo', 'shutdown', '-r', 'now'])


@app.command()
def shutdown(ctx: Context):
    '''
    Shutdown the VM
    '''
    if confirm('Are you sure you want to shutdown?'):
        if state.fake:
            print('Fake:shutting down the VM now')
        else:
            subprocess.run(['sudo', 'shutdown', '-h', 'now'])


@app.command()
def create(ctx: Context,
           container_name: Annotated[str, Argument(help="The name of the container", show_default=False)],
           ip_address: Annotated[str, Argument(help="The IP address of the container", show_default=False)]):
    '''
    Create new container
    '''

    non_interactive_command(['/snap/bin/lxc', 'init', 'ubuntu:22.04', container_name])
    non_interactive_command(['/snap/bin/lxc', 'network', 'attach', 'lxdbr0', container_name, 'eth0'])
    non_interactive_command(['/snap/bin/lxc', 'config', 'device', 'set', container_name, 'eth0', 'ipv4.address', ip_address])
    non_interactive_command(['/snap/bin/lxc', 'start', container_name])

    print(f'Created container {container_name} and started it')


@app.command()
def shell(ctx: Context,
          container_name: Annotated[str, Argument(help="The name of the container", show_default=False)],
          root: Annotated[bool, Option("--root", help="Login as root user")] = False):
    '''
    Access the shell for CONTAINER

    For "normal" user: shell CONTAINER

    For root user: shell --root CONTAINER
    '''
    if root:
        command = ['/snap/bin/lxc', 'shell', container_name]
    else:
        command = ['/snap/bin/lxc', 'exec', container_name, '--', 'su', '-', 'ubuntu']

    interactive_command(command, state.fake)


@app.command()
def start(ctx: Context,
          container_name: Annotated[str, Argument(help="The name of the container", show_default=False)]):
    '''
    Start the container CONTAINER
    '''
    non_interactive_command(['/snap/bin/lxc', 'start', container_name])
    print(f'Started {container_name}')


@app.command()
def stop(ctx: Context,
         container_name: Annotated[str, Argument(help="The name of the container", show_default=False)]):
    '''
    Stop the container CONTAINER
    '''
    non_interactive_command(['/snap/bin/lxc', 'stop', container_name])
    print(f'Stopped {container_name}')


@app.command()
def restart(ctx: Context,
            container_name: Annotated[str, Argument(help="The name of the container", show_default=False)]):
    '''
    Restart the container CONTAINER
    '''
    non_interactive_command(['/snap/bin/lxc', 'restart', container_name])
    print(f'Restarted {container_name}')


@app.command()
def delete(ctx: Context,
           container_name: Annotated[str, Argument(help="The name of the container", show_default=False)]):
    '''
    Delete the container CONTAINER
    '''
    non_interactive_command(['/snap/bin/lxc', 'stop', container_name])
    interactive_command(['/snap/bin/lxc', 'delete', '-i', container_name], state.fake)


@app.command()
def pull_file(ctx: Context,
              container_name: Annotated[str, Argument(help="The name of the container", show_default=False)],
              src_file: Annotated[str, Argument(help="The full path of the file inside the container (must start with a /)", show_default=False)],
              dest_name: Annotated[str, Argument(help="The name of the file in the VM", show_default=False)],):
    '''
    Pull a file FILE from the container CONTAINER
    '''
    ensure_file_store()
    if not src_file.startswith('/'):
        print('ERROR: Need to specify the full path in the src_file')
        return
    non_interactive_command(['/snap/bin/lxc', 'file', 'pull', f'{container_name}{src_file}', str(store_path.joinpath(dest_name))])


@app.command()
def push_file(ctx: Context,
              container_name: Annotated[str, Argument(help="The name of the container", show_default=False)],
              src_name: Annotated[str, Argument(help="The name of the file in the VM", show_default=False)],
              dest_file: Annotated[str, Argument(help="The full path of the file inside the container (must start with a /)", show_default=False)]):
    '''
    Push a file FILE into the container CONTAINER
    '''
    ensure_file_store()
    if not dest_file.startswith('/'):
        print('ERROR: Need to specify the full path in the dest_file')
        return
    non_interactive_command(['/snap/bin/lxc', 'file', 'push', str(store_path.joinpath(src_name)), f'{container_name}{dest_file}'])


@app.command()
def list_files(ctx: Context):
    '''
    List files available on local VM
    '''
    ensure_file_store()
    non_interactive_command(['/bin/ls', '-l', store_path])


@app.command()
def create_proxy_port(ctx: Context,
                      container_name: Annotated[str, Argument(help="The name of the container", show_default=False)],
                      container_port: Annotated[int, Argument(help="The port on the container to connect to", show_default=False)],
                      vm_port: Annotated[int, Argument(help="The port on the VM to listen on", show_default=False)]):
    '''
    Setup a proxy port from the VM port number VM_PORT to CONTAINER_PORT on the container CONTAINER_NAME
    '''
    non_interactive_command('/snap/bin/lxc', 'config', 'device', 'add', container_name, f'{container_name}{container_port}', 'proxy', f'listen=tcp:0.0.0.0:{vm_port}', f'connect=127.0.0.1:{container_port}')
    print(f'Forwarded port {vm_port} on the VM to {container_name}:{container_port}')


@app.command()
def delete_proxy_port(ctx: Context,
                      container_name: Annotated[str, Argument(help="The name of the container", show_default=False)],
                      container_port: Annotated[int, Argument(help="The port on the container that was forwarded", show_default=False)]):
    '''
    Delete a proxy port from the CONTAINER_PORT on the container CONTAINER_NAME
    '''
    non_interactive_command('/snap/bin/lxc', 'config', 'device', 'remove', container_name, f'{container_name}{container_port}')
    print(f'Removed proxy connection to {container_name}:{container_port}')


@app.command(hidden=True)
def nfs_server_config(ctx: Context,
                      container_name: Annotated[str, Argument(help="The name of the container", show_default=False)]):
    '''
    Configure CONTAINER as an NFS server
    '''
    non_interactive_command(['/snap/bin/lxc', 'config', 'set', container_name, 'security.privileged', 'true'])
    non_interactive_command(['/snap/bin/lxc', 'config', 'set', container_name, 'raw.apparmor', '"mount fstype=rpc_pipefs, mount fstype=nfsd, mount fstype=nfs,"'])
    non_interactive_command(['/snap/bin/lxc', 'restart', container_name])


@app.command(hidden=True)
def nfs_client_config(ctx: Context,
                      container_name: Annotated[str, Argument(help="The name of the container", show_default=False)]):
    '''
    Configure CONTAINER as an NFS client
    '''
    non_interactive_command(['/snap/bin/lxc', 'config', 'set', container_name, 'security.privileged', 'true'])
    non_interactive_command(['/snap/bin/lxc', 'config', 'set', container_name, 'raw.apparmor', '"mount fstype=nfs"'])
    non_interactive_command(['/snap/bin/lxc', 'restart', container_name])


if __name__ == "__main__":
    app()

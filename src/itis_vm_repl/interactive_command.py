# import os
# import sys
# import select
# import termios
# import tty
# import pty

from subprocess import call

Command = list[str]


# def interactive_command(command: Command, fake: bool = False):
#     # command = 'bash'
#     # command = 'docker run -it --rm centos /bin/bash'.split()

#     if fake:
#         print('Fake running command:')
#         print(' '.join(command))
#         return

#     # save original tty setting then set it to raw mode
#     old_tty = termios.tcgetattr(sys.stdin)
#     tty.setraw(sys.stdin.fileno())

#     # open pseudo-terminal to interact with subprocess
#     master_fd, slave_fd = pty.openpty()

#     try:
#         # use os.setsid() make it run in a new process group, or bash job control will not be enabled
#         p = Popen(command,
#                   preexec_fn=os.setsid,
#                   stdin=slave_fd,
#                   stdout=slave_fd,
#                   stderr=slave_fd,
#                   universal_newlines=True)

#         while p.poll() is None:
#             r, w, e = select.select([sys.stdin, master_fd], [], [], 1.0)
#             if sys.stdin in r:
#                 d = os.read(sys.stdin.fileno(), 10240)
#                 os.write(master_fd, d)
#             elif master_fd in r:
#                 o = os.read(master_fd, 10240)
#                 if o:
#                     os.write(sys.stdout.fileno(), o)
#     finally:
#         # restore tty settings back
#         termios.tcsetattr(sys.stdin, termios.TCSADRAIN, old_tty)

def interactive_command(command: Command, fake: bool = False):
    if fake:
        print('Fake running command:')
        print(' '.join(command))
        return
    call(command)

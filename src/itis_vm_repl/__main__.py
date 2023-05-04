# SPDX-FileCopyrightText: 2023-present Tom Moyer <tom.moyer@uncc.edu>
#
# SPDX-License-Identifier: MIT
import sys

if __name__ == "__main__":
    from itis_vm_repl.cli import itis_vm_repl

    sys.exit(itis_vm_repl())

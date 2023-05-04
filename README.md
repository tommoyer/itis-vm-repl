# ITIS VM REPL

[![PyPI - Version](https://img.shields.io/pypi/v/itis-vm-repl.svg)](https://pypi.org/project/itis-vm-repl)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/itis-vm-repl.svg)](https://pypi.org/project/itis-vm-repl)

-----

**Table of Contents**

- [Description](#description)
- [Installation](#installation)
- [License](#license)

## Description

This is the REPL that I use for my classes where students use LXC containers and VMs. The core idea is that they don't need to have shell access to the VM. Instead, the VM acts as a host for the containers and VMs and the REPL gives them a limited set of commands to run on the VM. This is so that students don't do things like install software in the VM when it should have been done in a container.

## Installation

```console
pipx install itis-vm-repl
```

## License

`itis-vm-repl` is distributed under the terms of the [MIT](https://spdx.org/licenses/MIT.html) license.

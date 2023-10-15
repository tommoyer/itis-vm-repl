#!/bin/bash

echo "Updating apt"
sudo apt update &> bootstrap.log
echo "Updating packages"
sudo apt dist-upgrade -y &> bootstrap.log
echo "Installing pipx"
sudo apt install pipx git -y &> bootstrap.log
pipx ensurepath
echo "Installing lxd"
sudo snap install lxd --channel=5.0/stable &> bootstrap.log
echo "Installing REPL"
pipx install git+https://github.com/tommoyer/itis-vm-repl.git

echo "Adding user to lxd group"
sudo adduser ubuntu lxd

echo "Adding escape-hatch user"
sudo adduser escape
sudo adduser escape lxd

echo "Setting up desktop file"
mkdir -p /home/ubuntu/.local/share/applications/
cat<<EOF > /home/ubuntu/.local/share/applications/itis-vm-repl.desktop
[Desktop Entry]
Version=1.0
Name=ITIS VM Shell
Exec=xfce4-terminal -x /home/ubuntu/.local/bin/repl
Icon=org.xfce.terminal
Terminal=false
Type=Application
Categories=GTK;System;TerminalEmulator;
StartupNotify=true

EOF

newgrp lxd

cat<<EOF | lxd init --preseed
config: {}
networks:
- config:
    dns.mode: none
    ipv4.address: 172.16.31.1/24
    ipv4.nat: "true"
    ipv6.address: none
  description: ""
  name: lxdbr0
  type: bridge
  project: default
storage_pools:
- config:
    source: /var/snap/lxd/common/lxd/storage-pools/default
  description: ""
  name: default
  driver: dir
profiles:
- config: {}
  description: Default LXD profile
  devices:
    eth0:
      nictype: bridged
      parent: lxdbr0
      type: nic
    root:
      path: /
      pool: default
      type: disk
  name: default
projects:
- config:
    features.images: "true"
    features.networks: "true"
    features.profiles: "true"
    features.storage.volumes: "true"
  description: Default LXD project
  name: default

EOF

update-desktop-database /home/ubuntu/.local/share/applications

echo "Done. Apply tweaks to UI"
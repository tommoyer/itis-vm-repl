#!/bin/bash

echo "Updating apt"
sudo apt update &> bootstrap.log
echo "Updating packages"
sudo apt dist-upgrade -y &> bootstrap.log
echo "Installing pipx"
sudo apt install pipx git -y &> bootstrap.log
echo "Installing lxd"
sudo snap install lxd --channel=5.0/stable &> bootstrap.log
echo "Installing REPL"
pipx install git+https://github.com/tommoyer/itis-3246-repl.git
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

update-desktop-database /home/ubuntu/.local/share/applications

echo "Adding user to lxd group"
sudo adduser ubuntu lxd

echo "Adding escape-hatch user"
sudo adduser escape
sudo adduser escape lxd

echo "Done. Apply tweaks to UI"
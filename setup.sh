#!/bin/bash

echo "> Setting up pipenv..."
pipenv sync

echo "> Configuring privileges..."
chmod +x arxive.sh
chmod +x update.sh

install_dir=$(pwd)
home_dir="$HOME"

echo "> Adding arXive to PATH..."
echo "export PATH=\"${install_dir}:\$PATH\"" >> ~/.profile
source "$home_dir"/.profile
if [ -e "$home_dir/.bashrc" ]; then
  echo "export PATH=\"${install_dir}:\$PATH\"" >> ~/.bashrc
  source "$home_dir"/.bashrc
elif [ -e "$home_dir/.zshrc" ]; then
  echo "export PATH=\"${install_dir}:\$PATH\"" >> ~/.zshrc
  source "$home_dir"/.zshrc
else
  echo "Warning: No .bashrc or .zshrc file found. The PATH has been written to ~/.profile."
fi
echo "$PATH"

echo "> Creating symlink..."
ln -s "$install_dir"/arxive.sh "$install_dir"/arxive

echo "> Creating desktop entry..."
cat >> ~/.local/share/applications/arxive.desktop <<EOF
[Desktop Entry]
Type=Application
Name=arXive
Exec=sh $install_dir/arxive.sh -g
Terminal=false
Icon=$install_dir/src/ui/arxive.svg
Categories=System
EOF

echo "> Creating configuration file..."
echo '{"source": "", "destination": "", "options": null}' >> ~/.config/arxive

echo "> Done. Goodbye!"

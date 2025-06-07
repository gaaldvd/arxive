echo "> Setting up pipenv..."
pipenv sync

echo "> Configuring privileges..."
chmod +x arxive.sh
chmod +x update.sh

install_dir=$(pwd)

echo "> Adding arXive to PATH..."
echo 'export PATH="'$install_dir':$PATH"' >> ~/.profile
source ~/.profile
echo $PATH

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

echo "> Done. Goodbye!"

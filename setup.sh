echo "> Setting up pipenv..."
pipenv sync

echo "> Configuring privileges..."
chmod +x arxive.sh
chmod +x update.sh

echo "> Done. Goodbye!"

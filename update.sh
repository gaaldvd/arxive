#!/bin/bash

echo "> Checking requirements..."
echo "> Python version: $(python --version)"
echo "> PIP version: $(pip --version)"
echo "> pipenv version: $(pipenv --version)"

# prompt for git update
until [ "$git_up" = "y" ] || [ "$git_up" = "Y" ] || [ "$git_up" = "n" ] || [ "$git_up" = "N" ]
do
  read -r -p "Update git repository? [y/n] " git_up
done

# prompt for env update
until [ "$pip_up" = "y" ] || [ "$pip_up" = "Y" ] || [ "$pip_up" = "n" ] || [ "$pip_up" = "N" ]
do
  read -r -p "Update python environment? [y/n] " pip_up
done

# update git repo
if [ "$git_up" = "y" ] || [ "$git_up" = "Y" ]
then
  echo "> Updating git repository..."
  git pull
  echo "> Git repository is up to date."
fi

# update env
if [ "$pip_up" = "y" ] || [ "$pip_up" = "Y" ]
then
  echo "> Updating python environment..."
  pipenv update
  echo "> Python environment is up to date."
fi

# verify packages
echo "> Pipfile verification... $(pipenv verify)"

# show package info
echo "> pyside6: $(pipenv run pip show pyside6)"

echo "> Done. Goodbye!"

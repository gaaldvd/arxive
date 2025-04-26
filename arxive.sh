# validate options
if [ "$#" -eq 0 ]; then
    echo "> Usage: $0 [-u] [-c/-g] [SOURCE] [DESTINATION]"
    exit 1
fi

# interpret options
while getopts "ucg" flag; do
  case $flag in
    u)
      echo "> Updating arXive..."
      ./update.sh
      exit 0;;
    c) mode="cli";;
    g) mode="gui";;
    *)
      echo "> Usage: $0 [-u] [-c/-g] [SOURCE] [DESTINATION]"
      exit 1;;
  esac
done

# start application
clear
pipenv run python src/arxive_"$mode".py

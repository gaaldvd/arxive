# validate options
if [ "$#" -eq 0 ] || [ "$#" -gt 3 ] || [[ "$1" != "-u" && "$1" != "-c" && "$1" != "-g" ]]; then
    echo "> Usage: arxive [-u] [-c / -g] [<SOURCE>] [<DESTINATION>]"
    exit 1
fi

SCRIPT_DIR=$(dirname "$(readlink -f "$0")")
cd "$SCRIPT_DIR" || exit

# interpret options
while getopts "ucg" flag; do
  case $flag in
    u)
      echo "> Updating arXive..."
      ./update.sh
      exit 0;;
    c)
      mode="cli"
      break;;
    g)
      mode="gui"
      break;;
    *)
      echo "> Usage: arxive [-u] [-c / -g] [<SOURCE>] [<DESTINATION>]"
      exit 1;;
  esac
done

# start application
clear
if [ -n "$2" ] && [ -n "$3" ]; then
    pipenv run python src/arxive_"$mode".py "$2" "$3"
    #pipenv run python src/test_"$mode".py "$2" "$3"
else
    echo "> No source/destination specified."
    echo "> Usage: arxive [-u] [-c / -g] [<SOURCE>] [<DESTINATION>]"
fi

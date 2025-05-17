# validate options
if [ "$#" -eq 0 ] || [ "$#" -gt 3 ] || [[ "$1" != "-u" && "$1" != "-c" && "$1" != "-g" ]]; then
    echo "> Usage: $0 [-u] [-c / -g] [<SOURCE>] [<DESTINATION>]"
    exit 1
fi

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
      echo "> Usage: $0 [-u] [-c / -g] [<SOURCE>] [<DESTINATION>]"
      exit 1;;
  esac
done

# start application
clear
if [ -n "$2" ] && [ -n "$3" ]; then
    echo "> Source: $2"
    echo "> Destination: $3"
    pipenv run python src/arxive_"$mode".py "$2" "$3"
    #pipenv run python src/test_"$mode".py "$2" "$3"
else
    echo "> No source/destination specified."
    pipenv run python src/arxive_"$mode".py
    #pipenv run python src/test_"$mode".py
fi

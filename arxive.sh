#!/bin/bash

usage() {
    echo "> Usage: arxive -c|-g|-u [-n] [<source> <destination>]"
    exit 1
}

if [ $# -lt 1 ]; then
    usage
fi

SCRIPT_DIR=$(dirname "$(readlink -f "$0")")
cd "$SCRIPT_DIR" || exit

mode=""
no_interrupt=false
source=""
destination=""

while [[ $# -gt 0 ]]; do
    case "$1" in
        -c|-g|-u)
            if [[ -n "$mode" ]]; then
                echo "> Error: Multiple modes specified."
                usage
            fi
            mode="$1"
            shift
            ;;
        -n)
            no_interrupt=true
            shift
            ;;
        *)
            if [[ -z "$source" ]]; then
                source="$1"
            elif [[ -z "$destination" ]]; then
                destination="$1"
            else
                echo "> Error: Too many arguments provided."
                usage
            fi
            shift
            ;;
    esac

done

if [[ -z "$mode" ]]; then
    echo "> Error: Mode (-c, -g, or -u) is required."
    usage
fi

case "$mode" in
    -c)
        mode="cli"
        ;;
    -g)
        mode="gui"
        ;;
    -u)
        echo "> Updating arXive..."
        ./update.sh
        exit 0;;
    *)
        echo "> Unexpected mode."
        usage
        ;;
esac

echo "> Welcome to arXive!"
echo "  Mode: $mode"
echo "  No Interrupt: $no_interrupt"
echo "  Source: $source"
echo "  Destination: $destination"

if $no_interrupt; then
    echo "  No interrupt option selected."
fi

if [[ -n "$source" && -n "$destination" ]]; then
    echo "  Syncing from $source to $destination..."
else
    echo "  Source and destination not specified."
fi

pipenv run python src/arxive_"$mode".py "$source" "$destination" "$no_interrupt"

#!/bin/bash

# Script that `touch`es all files under a directory, updating their time-stamps


usage="$(basename "$0") [-h] [-p] -- program to update time-stamps of all files underneath a directry recursively.

where:
    -h  show this help text
    -p  set the path to top directory (default: current directory)"


while getopts ":hp:" option
do
    case "${option}"
    in
    h) echo "$usage"
       exit
       ;;
    # set base path given by the user. Remove trailing slash if any.   
    p) BASE_PATH=${OPTARG%/}
       ;;
   \?) printf "illegal option: -%s\n" "$OPTARG" >&2
       echo "$usage" >&2
       exit 1
       ;;
    esac
done

if [ -z ${BASE_PATH+string} ]
then
    break=0
    while [ $break -eq 0 ]
    do
        read -p "No top directory path specified. Continue with current directory? [y/n] : " answer
        if [ "$answer" = "y" ]
        then
            BASE_PATH=.
            break=1
        elif [ "$answer" = "n" ]
        then
            exit 1
        else
            echo "Did not understand. Please input [y/n] : "
        fi
    done
        
fi

# Update time-stamp for top-level directory first
touch $BASE_PATH

echo "Updating time-stamp for files in \"${BASE_PATH}\""

for item in `ls -a ${BASE_PATH}`
do
    # If file then `touch` it
    if [ -f "${BASE_PATH}/${item}" ]
    then
        touch "${BASE_PATH}/${item}"
    # Ignore parent and current directory. Prevents getting caught in loop
    elif [ ${item} = "." -o ${item} = ".." ]
    then
        # Simply ignore; do nothing.
        :
    # Recursively call the script on nested directories
    elif [ -d "${BASE_PATH}/${item}" ] 
    then
        touch "${BASE_PATH}/${item}"
        echo "$($0 -p ${BASE_PATH}/${item})"
    fi
done
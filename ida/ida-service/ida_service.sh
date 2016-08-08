#!/usr/bin/env bash

re='^[0-9]+$'

while :
do
    case "$1" in
      -c | --core)
    	  CORES="$2"
        if [ -z ${CORES} ]; then
          echo "Error: cores must be set" >&2; exit 1
        fi
        if ! [[ $CORES =~ $re ]] ; then
          echo "Error: $CORES is not a number" >&2; exit 1
        fi
    	  shift 2
    	  ;;
      -t | --timeout)
    	  TIMEOUT="$2"
        if [ -z ${TIMEOUT} ]; then
          echo "Error: timeout must be set" >&2; exit 1
        fi
        if ! [[ $TIMEOUT =~ $re ]] ; then
          echo "Error: $TIMEOUT is not a number" >&2; exit 1
        fi
    	  shift 2
    	  ;;
      ?*)
        echo "Error: Unknown option: $1" >&2; exit 1
        ;;
      *)  # No more options
    	  break
    	  ;;
    esac
done


if [ -z ${CORES+x} ]; then CORES=8;fi
if [ -z ${TIMEOUT+x} ]; then TIMEOUT=30;fi

gunicorn -w $CORES -t $TIMEOUT -b 0.0.0.0:4000 flask_service:app

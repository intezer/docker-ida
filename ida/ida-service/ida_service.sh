#!/usr/bin/env bash

while :
do
    case "$1" in
      -c | --core)
    	  CORES="$2"
    	  shift 2
    	  ;;
      -t | --timeout)
    	  TIMEOUT="$2"
    	  shift 2
    	  ;;
      --)
        shift
        break;
        ;;
      -*)
        echo "Error: Unknown option: $1" >&2
        exit 1
        ;;
      *)  # No more options
    	  break
    	  ;;
    esac
done


if [ -z ${CORES+x} ]; then CORES=8;fi
if [ -z ${TIMEOUT+x} ]; then TIMEOUT=30;fi

gunicorn -w $CORES -t $TIMEOUT -b 0.0.0.0:4000 flask_service:app

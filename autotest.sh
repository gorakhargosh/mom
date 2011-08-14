#!/bin/sh
#
# You will need watchdog installed for this to work.
watchmedo shell-command \
    --patterns="*.idea;*.py;*.c" \
    --recursive \
    --command='tox -e py27' \
    .

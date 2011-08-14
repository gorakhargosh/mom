#!/bin/sh

watchmedo shell-command --patterns="*.idea;*.py;*.c" --recursive --command='tox -e py27' .

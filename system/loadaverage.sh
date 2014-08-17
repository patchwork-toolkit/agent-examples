#!/bin/bash

uptime | awk -F'[a-z]:' '{ print $2}' | sed -e 's/^ *//' -e 's/ *$//'

exit 0
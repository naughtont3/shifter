#!/bin/sh

set -v

curl -H "authentication: $(munge -n)" http://api:5000/api/list/systema/

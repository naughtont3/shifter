#!/bin/sh

set -v

curl -H "authentication: $(munge -n)" -X POST http://api:5000/api/pull/systema/docker/naughtont3/bb-hellosleep:latest/

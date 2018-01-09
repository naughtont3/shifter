#!/bin/sh

set -v

curl -H "authentication: $(munge -n)" -d '{"filePath":"/tmp/testing/tjntest.save.tar","format":"squashfs"}' http://api:5000/api/load/systema/docker/tjntest:latest/

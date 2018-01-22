#!/bin/sh

mkdir -p /tmp/testing/
cp test/save-tars/naughtont3-tjntest.save.tar /tmp/testing/tjntest.save.tar
chmod a+r /tmp/testing/tjntest.save.tar

ls -l /tmp/testing/tjntest.save.tar

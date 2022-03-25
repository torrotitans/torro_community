#!/usr/bin/env bash

cd engine
cp -rf torro.service /etc/systemd/system/
systemctl start torro.service
systemctl enable torro.service
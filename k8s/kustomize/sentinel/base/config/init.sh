#!/bin/bash
cp /sentinel-config/sentinel.conf /shared-config/sentinel.conf
chmod 777 /shared-config/sentinel.conf

while ! ping -c 1 redis-0.redis; do
	echo 'Waiting for server'
	sleep 1
done
#!/bin/bash

mkdir -p ~/.ssh
cp /mysql-sshkey/mysql-sshkey ~/.ssh/id_rsa
cp /mysql-sshkey/mysql-sshkey.pub ~/.ssh/id_rsa.pub
cp /mysql-sshkey/mysql-sshknown_hosts ~/.ssh/known_hosts
chmod 700 ~/.ssh
chmod 600 ~/.ssh/id_rsa
chmod 644 ~/.ssh/id_rsa.pub
chmod 644 ~/.ssh/known_hosts

echo '[STEP 1] ssh key configured'

if [ -n "${MYSQL_SSH_HOST}" ]; then
  autossh -f -N -M 0 -L $MYSQL_PORT:$MYSQL_HOST:$MYSQL_PORT -p $MYSQL_SSH_PORT $MYSQL_SSH_USER@$MYSQL_SSH_HOST

  echo '[STEP 2] ssh tunnel configured'
fi
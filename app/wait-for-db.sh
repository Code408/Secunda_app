#!/bin/sh

set -e

host="$1"
shift
cmd="$@"

echo "Waiting for MySQL at $host..."

until mysqladmin ping -h "$host" -u root -p12345 --silent; do
  >&2 echo "MySQL is unavailable - sleeping"
  sleep 1
done

echo "MySQL is up - executing command"
exec $cmd
#!/bin/sh

cat <<EOF
[database]
USER:     ${DB_USER}
PASSWORD: ${DB_PASSWORD}
NAME:     ${DB_NAME}
HOST:     db
PORT:     5432
EOF
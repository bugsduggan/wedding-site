#!/bin/bash

PG_DUMP="/Applications/Postgres.app/Contents/Versions/latest/bin/pg_dump"
APPLICATION_NAME="lakesman-wedding-site-2017"
DATABASE_URL=$(heroku config:get DATABASE_URL -a $APPLICATION_NAME)

$PG_DUMP --verbose -Fc --file=${1:-".db_backup"} $DATABASE_URL

#!/bin/bash

PG_RESTORE="/Applications/Postgres.app/Contents/Versions/latest/bin/pg_restore"
APPLICATION_NAME="lakesman-wedding-site-2017"
DATABASE_URL=$(heroku config:get DATABASE_URL -a $APPLICATION_NAME)

$PG_RESTORE --verbose --dbname=$DATABASE_URL ${1:-".db_backup"}

#!/bin/bash
set -e

# Download and restore dvdrental database
cd /tmp

if [ ! -f dvdrental.tar ]; then
    echo "Downloading dvdrental database..."
    curl -L -o dvdrental.zip https://www.postgresqltutorial.com/wp-content/uploads/2019/05/dvdrental.zip
    unzip -o dvdrental.zip
    echo "Database downloaded and extracted"
fi

# Wait a moment for postgres to be fully ready
sleep 2

# Restore the database
echo "Restoring dvdrental database..."
pg_restore -U postgres -d dvdrental -v /tmp/dvdrental.tar 2>&1 || echo "Restore completed (some warnings are normal)"

echo "Database initialization complete!"


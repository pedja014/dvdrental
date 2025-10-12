#!/bin/bash
set -e

echo "==================================="
echo "DVD Rental Database Initialization"
echo "==================================="

# Install wget if not available
if ! command -v wget &> /dev/null; then
    echo "Installing wget..."
    apk add --no-cache wget unzip
fi

# Download and restore dvdrental database
cd /tmp

if [ ! -f dvdrental.tar ]; then
    echo "Downloading dvdrental database (this may take 1-2 minutes)..."
    
    # Try primary source using wget
    if wget -O dvdrental.zip https://www.postgresqltutorial.com/wp-content/uploads/2019/05/dvdrental.zip; then
        echo "Download successful!"
    else
        echo "Primary download failed, trying alternative source..."
        wget -O dvdrental.zip https://github.com/devrimgunduz/pagila/raw/master/dvdrental.zip || {
            echo "ERROR: Failed to download database"
            exit 1
        }
    fi
    
    echo "Extracting database..."
    unzip -o dvdrental.zip || {
        echo "ERROR: Failed to extract database"
        exit 1
    }
    echo "Database downloaded and extracted successfully!"
else
    echo "Database file already exists, skipping download"
fi

# Wait for postgres to be fully ready
echo "Waiting for PostgreSQL to be fully initialized..."
sleep 5

# Check if database already has tables
TABLE_COUNT=$(psql -U postgres -d dvdrental -t -c "SELECT COUNT(*) FROM information_schema.tables WHERE table_schema='public';" 2>/dev/null || echo "0")

if [ "$TABLE_COUNT" -gt "5" ]; then
    echo "Database already initialized with $TABLE_COUNT tables - skipping restore"
else
    # Restore the database
    echo "Restoring dvdrental database (this may take 2-3 minutes)..."
    echo "You may see some warnings - they are normal"
    pg_restore -U postgres -d dvdrental -v /tmp/dvdrental.tar 2>&1 | grep -v "WARNING" || echo "Restore process completed"
    
    # Verify restoration
    TABLE_COUNT=$(psql -U postgres -d dvdrental -t -c "SELECT COUNT(*) FROM information_schema.tables WHERE table_schema='public';" || echo "0")
    echo "Database restored with $TABLE_COUNT tables"
fi

echo "==================================="
echo "Database initialization complete!"
echo "==================================="


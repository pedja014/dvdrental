#!/bin/sh
set -e

# Load dvdrental sample database on first init if requested.

echo "[dvdrental-init] Starting dvdrental initialization script..."

LOAD_FLAG="${LOAD_DVDRENTAL:-false}"
TARGET_DB="${DVDRENTAL_DB:-dvdrental_sample}"
POSTGRES_USER="${POSTGRES_USER:-postgres}"

case "$(printf "%s" "$LOAD_FLAG" | tr '[:upper:]' '[:lower:]')" in
  1|true|yes|on) ;;
  *)
    echo "[dvdrental-init] LOAD_DVDRENTAL is not enabled. Skipping dvdrental restore."
    exit 0
    ;;
esac

ARCHIVE_PATH="/docker-entrypoint-initdb.d/dvdrental.tar"

if [ ! -f "$ARCHIVE_PATH" ]; then
  if [ -n "$DVDRENTAL_URL" ]; then
    echo "[dvdrental-init] Downloading dvdrental from URL: $DVDRENTAL_URL"
    wget -O /tmp/dvdrental.tar "$DVDRENTAL_URL"
    ARCHIVE_PATH="/tmp/dvdrental.tar"
  else
    echo "[dvdrental-init] No dvdrental.tar found and no DVDRENTAL_URL provided. Skipping."
    exit 0
  fi
fi

echo "[dvdrental-init] Creating database '$TARGET_DB'..."
createdb -U "$POSTGRES_USER" "$TARGET_DB" || true

echo "[dvdrental-init] Restoring dvdrental into '$TARGET_DB'..."
pg_restore -U "$POSTGRES_USER" -d "$TARGET_DB" "$ARCHIVE_PATH"

echo "[dvdrental-init] dvdrental restore completed."



#!/bin/sh
set -e

# Create database views in dvdrental_sample database
# This script runs after the database is restored

TARGET_DB="${DVDRENTAL_DB:-dvdrental_sample}"
POSTGRES_USER="${POSTGRES_USER:-postgres}"

echo "[views-init] Creating views in database '$TARGET_DB'..."

# Wait for database to be ready (check if it exists)
i=0
while [ $i -lt 30 ]; do
    if psql -U "$POSTGRES_USER" -lqt 2>/dev/null | cut -d \| -f 1 | grep -qw "$TARGET_DB"; then
        echo "[views-init] Database '$TARGET_DB' found, creating views..."
        break
    fi
    i=$((i + 1))
    if [ $i -eq 30 ]; then
        echo "[views-init] WARNING: Database '$TARGET_DB' not found after waiting. Skipping views creation."
        exit 0
    fi
    sleep 1
done

psql -v ON_ERROR_STOP=1 -U "$POSTGRES_USER" -d "$TARGET_DB" <<-EOSQL
    -- View: film_with_categories
    -- Joins film, film_category, and category to provide films with their associated categories
    CREATE OR REPLACE VIEW film_with_categories AS
    SELECT 
        f.film_id,
        f.title,
        f.description,
        f.release_year,
        f.rental_duration,
        f.rental_rate,
        f.length,
        f.replacement_cost,
        f.rating,
        ARRAY_AGG(DISTINCT c.category_id) FILTER (WHERE c.category_id IS NOT NULL) AS category_ids,
        ARRAY_AGG(DISTINCT c.name) FILTER (WHERE c.name IS NOT NULL) AS category_names,
        f.last_update
    FROM film f
    LEFT JOIN film_category fc ON f.film_id = fc.film_id
    LEFT JOIN category c ON fc.category_id = c.category_id
    GROUP BY f.film_id, f.title, f.description, f.release_year, 
             f.rental_duration, f.rental_rate, f.length, 
             f.replacement_cost, f.rating, f.last_update;

    -- View: rental_with_payment_info
    -- Joins rental and payment for easier access to payment data
    CREATE OR REPLACE VIEW rental_with_payment_info AS
    SELECT 
        r.rental_id,
        r.rental_date,
        r.inventory_id,
        r.customer_id,
        r.return_date,
        r.staff_id,
        COALESCE(SUM(p.amount), 0) AS total_payment_amount,
        COUNT(p.payment_id) AS payment_count,
        r.last_update
    FROM rental r
    LEFT JOIN payment p ON r.rental_id = p.rental_id
    GROUP BY r.rental_id, r.rental_date, r.inventory_id, 
             r.customer_id, r.return_date, r.staff_id, r.last_update;

    -- View: rental_with_film_info
    -- Joins rental, inventory, and film to provide film details in rental context
    CREATE OR REPLACE VIEW rental_with_film_info AS
    SELECT 
        r.rental_id,
        r.rental_date,
        r.customer_id,
        r.return_date,
        r.staff_id,
        i.inventory_id,
        i.film_id,
        f.title AS film_title,
        f.rental_rate,
        r.last_update
    FROM rental r
    JOIN inventory i ON r.inventory_id = i.inventory_id
    JOIN film f ON i.film_id = f.film_id;
EOSQL

echo "[views-init] Views created successfully in '$TARGET_DB'."


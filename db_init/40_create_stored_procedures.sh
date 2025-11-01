#!/bin/sh
set -e

# Create stored procedures in dvdrental_sample database
# This script runs after the database is restored

TARGET_DB="${DVDRENTAL_DB:-dvdrental_sample}"
POSTGRES_USER="${POSTGRES_USER:-postgres}"

echo "[procedures-init] Creating stored procedures in database '$TARGET_DB'..."

# Wait for database to be ready (check if it exists)
i=0
while [ $i -lt 30 ]; do
    if psql -U "$POSTGRES_USER" -lqt 2>/dev/null | cut -d \| -f 1 | grep -qw "$TARGET_DB"; then
        echo "[procedures-init] Database '$TARGET_DB' found, creating stored procedures..."
        break
    fi
    i=$((i + 1))
    if [ $i -eq 30 ]; then
        echo "[procedures-init] WARNING: Database '$TARGET_DB' not found after waiting. Skipping procedures creation."
        exit 0
    fi
    sleep 1
done

psql -v ON_ERROR_STOP=1 -U "$POSTGRES_USER" -d "$TARGET_DB" <<-EOSQL
    -- Procedure: get_most_profitable_categories_by_year
    -- Returns most profitable movie categories grouped by year
    CREATE OR REPLACE FUNCTION get_most_profitable_categories_by_year(
        target_year INTEGER DEFAULT NULL
    )
    RETURNS TABLE (
        category_id INTEGER,
        category_name VARCHAR(25),
        year INTEGER,
        total_revenue NUMERIC(10,2),
        rental_count BIGINT,
        film_count BIGINT
    ) 
    LANGUAGE plpgsql
    AS \$\$
    BEGIN
        RETURN QUERY
        SELECT 
            c.category_id,
            c.name::VARCHAR(25) AS category_name,
            EXTRACT(YEAR FROM p.payment_date)::INTEGER AS year,
            SUM(p.amount)::NUMERIC(10,2) AS total_revenue,
            COUNT(DISTINCT r.rental_id)::BIGINT AS rental_count,
            COUNT(DISTINCT f.film_id)::BIGINT AS film_count
        FROM payment p
        JOIN rental r ON p.rental_id = r.rental_id
        JOIN inventory i ON r.inventory_id = i.inventory_id
        JOIN film f ON i.film_id = f.film_id
        JOIN film_category fc ON f.film_id = fc.film_id
        JOIN category c ON fc.category_id = c.category_id
        WHERE (target_year IS NULL OR EXTRACT(YEAR FROM p.payment_date) = target_year)
        GROUP BY c.category_id, c.name, EXTRACT(YEAR FROM p.payment_date)
        ORDER BY year DESC, total_revenue DESC;
    END;
    \$\$;

    -- Procedure: get_most_profitable_films_by_year
    -- Returns most profitable movies grouped by year
    CREATE OR REPLACE FUNCTION get_most_profitable_films_by_year(
        target_year INTEGER DEFAULT NULL,
        limit_count INTEGER DEFAULT 100
    )
    RETURNS TABLE (
        film_id INTEGER,
        title VARCHAR(255),
        year INTEGER,
        total_revenue NUMERIC(10,2),
        rental_count BIGINT,
        category_names TEXT[]
    ) 
    LANGUAGE plpgsql
    AS \$\$
    BEGIN
        RETURN QUERY
        SELECT 
            f.film_id,
            f.title::VARCHAR(255),
            EXTRACT(YEAR FROM p.payment_date)::INTEGER AS year,
            SUM(p.amount)::NUMERIC(10,2) AS total_revenue,
            COUNT(DISTINCT r.rental_id)::BIGINT AS rental_count,
            ARRAY_AGG(DISTINCT c.name) FILTER (WHERE c.name IS NOT NULL)::TEXT[] AS category_names
        FROM payment p
        JOIN rental r ON p.rental_id = r.rental_id
        JOIN inventory i ON r.inventory_id = i.inventory_id
        JOIN film f ON i.film_id = f.film_id
        LEFT JOIN film_category fc ON f.film_id = fc.film_id
        LEFT JOIN category c ON fc.category_id = c.category_id
        WHERE (target_year IS NULL OR EXTRACT(YEAR FROM p.payment_date) = target_year)
        GROUP BY f.film_id, f.title, EXTRACT(YEAR FROM p.payment_date)
        ORDER BY year DESC, total_revenue DESC
        LIMIT limit_count;
    END;
    \$\$;
EOSQL

echo "[procedures-init] Stored procedures created successfully in '$TARGET_DB'."


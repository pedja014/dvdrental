# Quick Start Guide

## Get Up and Running in 3 Steps

### Step 1: Start Docker Containers

```bash
docker-compose up --build
```

Wait for the initialization to complete (about 2-3 minutes). You'll see:
- PostgreSQL downloading and restoring the dvdrental database
- Django running migrations
- Superuser being created
- Server starting on http://localhost:8000

### Step 2: Access the API

Open your browser and go to:
- **Swagger UI**: http://localhost:8000/swagger/
- **API**: http://localhost:8000/api/

### Step 3: Authenticate in Swagger

1. In Swagger UI, click the **"Authorize"** button (top right)
2. Login first to get a token:
   - Go to `/api/auth/login/` endpoint
   - Click "Try it out"
   - Use credentials:
     ```json
     {
       "username": "admin",
       "password": "admin123"
     }
     ```
   - Execute and copy the `access` token from the response
3. Click "Authorize" button again
4. Paste: `Bearer <your-access-token>`
5. Click "Authorize"

Now you can test all API endpoints! 🎉

## Test the API with Python

```bash
# Install requests if needed
pip install requests

# Run the test script
python test_api.py
```

## Common Commands

```bash
# Stop containers
docker-compose down

# View logs
docker-compose logs -f

# Access Django shell
docker-compose exec web python manage.py shell

# Create a new superuser
docker-compose exec web python manage.py createsuperuser

# Run tests
docker-compose exec web python manage.py test
```

## Exploring the Database

The dvdrental database includes:
- 🎬 **1,000 films** with details (title, description, rating, rental rate, etc.)
- 🎭 **200 actors** linked to films
- 🗂️ **16 categories** (Action, Comedy, Drama, etc.)
- 👥 **599 customers**
- 📦 **4,581 inventory** items
- 📝 **16,044 rentals**
- 💰 **14,596 payments**
- 🏪 **2 stores**
- 👔 **2 staff** members

## API Highlights

### Browse the Catalog
```
GET /api/films/
GET /api/actors/
GET /api/categories/
```

### Search Films
```
GET /api/films/search/?q=love
```

### View Actor's Films
```
GET /api/actors/{id}/films/
```

### Manage Rentals (Staff/Admin)
```
GET /api/rentals/
GET /api/rentals/active/
POST /api/rentals/{id}/return_rental/
```

### Check Available Inventory
```
GET /api/inventory/available/
```

## User Roles

- **admin**: Full access (default user)
- **staff**: Manage rentals, inventory, customers
- **customer**: View catalog and own rentals

## Need Help?

See the full [README.md](README.md) for detailed documentation.


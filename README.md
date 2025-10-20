# DVD Rental API

A comprehensive REST API for managing a DVD rental business, built with Django REST Framework, PostgreSQL, and Docker. Features JWT authentication, role-based access control, and interactive Swagger documentation.

## Features

- 🎬 **Complete DVD Rental Management**: Films, actors, customers, rentals, payments, and more
- 🔐 **JWT Authentication**: Secure token-based authentication with refresh tokens
- 👥 **Role-Based Access Control**: Admin, Staff, and Customer roles with different permissions
- 📚 **Interactive API Documentation**: Swagger UI and ReDoc
- 🐳 **Docker Support**: Fully containerized application with Docker Compose
- 🗄️ **PostgreSQL Database**: Using the official PostgreSQL dvdrental sample database
- 🔍 **Advanced Features**: Search, filtering, pagination, and custom endpoints

## Technology Stack

- **Backend**: Django 4.2, Django REST Framework 3.14
- **Authentication**: djangorestframework-simplejwt 5.3
- **Database**: PostgreSQL 15
- **Documentation**: drf-yasg 1.21
- **Containerization**: Docker & Docker Compose
- **Web Server**: Gunicorn

## Quick Start

### Prerequisites

- Docker Desktop installed on your system
- Git (to clone the repository)

### Installation & Setup

1. **Clone the repository** (or ensure you're in the project directory):
   ```bash
   cd E:\dvdrental
   ```

2. **Copy environment template and set variables**:
   ```bash
   cp .env.example .env
   # edit .env and set SECRET_KEY, passwords, etc.
   ```

3. **Build and start the containers**:
   ```bash
   docker-compose up --build
   ```

   This will:
   - Download and set up PostgreSQL with the dvdrental sample database
   - Build the Django application
   - Run database migrations
   - Create a default superuser (from `.env`: `ADMIN_USERNAME`, `ADMIN_PASSWORD`)
   - Start the API server on http://localhost:8000

3. **Access the application**:
   - **API Base URL**: http://localhost:8000/api/
   - **Swagger Documentation**: http://localhost:8000/swagger/
   - **ReDoc Documentation**: http://localhost:8000/redoc/
   - **Django Admin**: http://localhost:8000/admin/

### Access Credentials

The initial superuser is configured via `.env` (`ADMIN_USERNAME`, `ADMIN_PASSWORD`). Do not commit real credentials.

## API Documentation

### Authentication Endpoints

| Endpoint | Method | Description | Auth Required |
|----------|--------|-------------|---------------|
| `/api/auth/register/` | POST | Register a new user | No |
| `/api/auth/login/` | POST | Login and get JWT tokens | No |
| `/api/auth/token/refresh/` | POST | Refresh access token | No |

### Main API Endpoints

| Resource | Endpoint | Methods | Description |
|----------|----------|---------|-------------|
| Films | `/api/films/` | GET, POST, PUT, PATCH, DELETE | Manage films |
| Actors | `/api/actors/` | GET, POST, PUT, PATCH, DELETE | Manage actors |
| Categories | `/api/categories/` | GET, POST, PUT, PATCH, DELETE | Manage categories |
| Customers | `/api/customers/` | GET, POST, PUT, PATCH, DELETE | Manage customers |
| Rentals | `/api/rentals/` | GET, POST, PUT, PATCH, DELETE | Manage rentals |
| Payments | `/api/payments/` | GET, POST, PUT, PATCH, DELETE | Manage payments |
| Inventory | `/api/inventory/` | GET, POST, PUT, PATCH, DELETE | Manage inventory |
| Staff | `/api/staff/` | GET, POST, PUT, PATCH, DELETE | Manage staff |
| Stores | `/api/stores/` | GET, POST, PUT, PATCH, DELETE | Manage stores |
| Addresses | `/api/addresses/` | GET, POST, PUT, PATCH, DELETE | Manage addresses |
| Cities | `/api/cities/` | GET, POST, PUT, PATCH, DELETE | Manage cities |
| Countries | `/api/countries/` | GET, POST, PUT, PATCH, DELETE | Manage countries |
| Languages | `/api/languages/` | GET, POST, PUT, PATCH, DELETE | Manage languages |

### Custom Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/users/me/` | GET | Get current user details |
| `/api/films/search/?q=<query>` | GET | Search films by title or description |
| `/api/actors/{id}/films/` | GET | Get all films for an actor |
| `/api/categories/{id}/films/` | GET | Get all films in a category |
| `/api/customers/{id}/rentals/` | GET | Get all rentals for a customer |
| `/api/customers/{id}/payments/` | GET | Get all payments for a customer |
| `/api/inventory/available/` | GET | Get available inventory |
| `/api/rentals/active/` | GET | Get active rentals |
| `/api/rentals/{id}/return_rental/` | POST | Mark a rental as returned |

## Usage Examples

### 1. Register a New User

```bash
curl -X POST http://localhost:8000/api/auth/register/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "johndoe",
    "email": "john@example.com",
    "password": "securepass123",
    "password2": "securepass123",
    "first_name": "John",
    "last_name": "Doe",
    "role": "customer"
  }'
```

### 2. Login and Get JWT Token

```bash
curl -X POST http://localhost:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "admin",
    "password": "admin123"
  }'
```

Response:
```json
{
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "access": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

### 3. Get Films List (Authenticated)

```bash
curl -X GET http://localhost:8000/api/films/ \
  -H "Authorization: Bearer <your_access_token>"
```

### 4. Search Films

```bash
curl -X GET "http://localhost:8000/api/films/search/?q=love" \
  -H "Authorization: Bearer <your_access_token>"
```

### 5. Get Available Inventory

```bash
curl -X GET http://localhost:8000/api/inventory/available/ \
  -H "Authorization: Bearer <your_access_token>"
```

### 6. Create a New Rental (Staff/Admin Only)

```bash
curl -X POST http://localhost:8000/api/rentals/ \
  -H "Authorization: Bearer <your_access_token>" \
  -H "Content-Type: application/json" \
  -d '{
    "inventory": 1,
    "customer": 1,
    "staff": 1,
    "rental_date": "2024-01-15T10:00:00Z"
  }'
```

## User Roles and Permissions

### Admin
- Full access to all endpoints
- Can manage users, staff, and all system resources
- Can view, create, update, and delete any record

### Staff
- Can manage inventory, rentals, and payments
- Can view and update customer information
- Can process rentals and returns
- Cannot manage other staff members or users

### Customer
- Can view the film catalog (read-only)
- Can view their own rental history
- Can view their own payment history
- Limited write access

## Database Schema

The API uses the official PostgreSQL dvdrental sample database with the following main tables:

- **actor**: Film actors
- **film**: Movie catalog
- **category**: Film categories
- **film_actor**: Many-to-many relationship between films and actors
- **film_category**: Many-to-many relationship between films and categories
- **customer**: Customer information
- **rental**: Rental transactions
- **payment**: Payment records
- **inventory**: Available film copies
- **staff**: Staff members
- **store**: Store locations
- **address, city, country**: Location data
- **language**: Film languages

## Development

### Running Commands in Docker

Execute Django management commands:
```bash
docker-compose exec web python manage.py <command>
```

Examples:
```bash
# Create migrations
docker-compose exec web python manage.py makemigrations

# Run migrations
docker-compose exec web python manage.py migrate

# Create superuser
docker-compose exec web python manage.py createsuperuser

# Access Django shell
docker-compose exec web python manage.py shell

# Collect static files
docker-compose exec web python manage.py collectstatic
```

### View Logs

```bash
# All services
docker-compose logs -f

# Only web service
docker-compose logs -f web

# Only database service
docker-compose logs -f db
```

### Stop the Application

```bash
# Stop containers
docker-compose down

# Stop and remove volumes (WARNING: This deletes the database)
docker-compose down -v
```

### Rebuild After Code Changes

```bash
docker-compose up --build
```

## Swagger UI Usage

1. Navigate to http://localhost:8000/swagger/
2. Click on the "Authorize" button at the top right
3. Get a token from `/api/auth/login/`
4. Enter: `Bearer <your_access_token>` in the authorization dialog
5. Now you can test all authenticated endpoints directly from Swagger UI

## Project Structure

```
dvdrental/
├── api/                          # Main API application
│   ├── migrations/               # Database migrations
│   ├── __init__.py
│   ├── admin.py                  # Admin interface configuration
│   ├── apps.py                   # App configuration
│   ├── models.py                 # Database models
│   ├── permissions.py            # Custom permissions
│   ├── serializers.py            # API serializers
│   ├── urls.py                   # API URL routing
│   └── views.py                  # API views and viewsets
├── dvdrental_project/            # Django project settings
│   ├── __init__.py
│   ├── asgi.py
│   ├── settings.py               # Project settings
│   ├── urls.py                   # Main URL configuration
│   └── wsgi.py
├── .env.example                  # Environment variables template
├── .gitignore                    # Git ignore rules
├── docker-compose.yml            # Docker Compose configuration
├── Dockerfile                    # Docker image definition
├── entrypoint.sh                 # Container entrypoint script
├── init-db.sh                    # Database initialization script
├── manage.py                     # Django management script
├── README.md                     # This file
└── requirements.txt              # Python dependencies
```

## Troubleshooting

### Database Connection Issues

If you see database connection errors:
1. Make sure PostgreSQL container is running: `docker-compose ps`
2. Check database logs: `docker-compose logs db`
3. Restart the services: `docker-compose restart`

### Port Already in Use

If port 8000 or 5432 is already in use:
1. Stop the conflicting service
2. Or modify the ports in `docker-compose.yml`

### Reset Database

To completely reset the database:
```bash
docker-compose down -v
docker-compose up --build
```

## pgAdmin (Optional)

Start pgAdmin UI:
```bash
docker compose up -d pgadmin
```

Open `http://localhost:5050` and log in with:
- Email: `admin@example.com`
- Password: `admin123`

Add a connection:
- Name: `dvdrental`
- Host: `db`
- Port: `5432`
- Username: `postgres`
- Password: `postgres123`

If 5050 is taken, change the mapping in `docker-compose.yml` (e.g., `"5051:80"`).

### pgAdmin troubleshooting: preconfigured server not visible
pgAdmin reads `servers.json` only on the first run. If you don't see the "dvdrental" server:

```bash
docker compose stop pgadmin
docker compose rm -f -v pgadmin
# remove its data volume (name may differ; list with: docker volume ls | grep pgadmin)
docker volume rm dvdrental_pgadmin_data || true
docker compose up -d pgadmin
```

Reopen `http://localhost:5050` and log in.

### dvdrental tables missing (e.g., "relation 'actor' does not exist")
If Admin or API pages fail with `ProgrammingError: relation "actor" does not exist`, your Postgres volume already existed and the `init-db.sh` import did not run. Reset the volume to trigger a fresh dvdrental restore:

```bash
docker compose down -v   # WARNING: deletes database volume
docker compose up --build
```

After start, verify data is present:

```bash
docker compose exec db psql -U postgres -d dvdrental -c "select count(*) from actor;"
```

## Production Considerations

Before deploying to production:

1. **Change Secret Key**: Set a strong `SECRET_KEY` in environment variables
2. **Disable Debug**: Set `DEBUG=False`
3. **Configure ALLOWED_HOSTS**: Add your domain to `ALLOWED_HOSTS`
4. **Use Strong Passwords**: Change default database and admin passwords
5. **Enable HTTPS**: Use a reverse proxy (nginx) with SSL certificates
6. **Configure CORS**: Restrict `CORS_ALLOW_ALL_ORIGINS` to specific domains
7. **Database Backups**: Implement regular database backup strategy
8. **Security Headers**: Add security middleware and headers
9. **Rate Limiting**: Implement API rate limiting
10. **Monitoring**: Set up logging and monitoring

## License

This project is open source and available under the MIT License.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Support

For issues, questions, or contributions, please create an issue in the repository.

## Acknowledgments

- PostgreSQL Tutorial for the dvdrental sample database
- Django and Django REST Framework communities
- All contributors and users of this project


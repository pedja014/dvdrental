# Authentication API

A clean, minimal Django REST API focused solely on authentication functionality.

## Quick Start

```bash
# Start the system
docker compose up --build

# Access the API
# 🚀 START HERE: Swagger UI (Interactive Testing): http://localhost:8000/api/docs/
# 📚 Documentation: http://localhost:8000/api/redoc/
# 🔧 API Schema: http://localhost:8000/api/schema/
```

**Note:** The system will automatically create the database tables and a superuser account on first run.

## 🧪 How to Test the API

1. **Go to Swagger UI:** `http://localhost:8000/api/docs/`
2. **Register a user:**
   - Click `POST /api/auth/register/`
   - Click "Try it out"
   - Enter user data and click "Execute"
3. **Login to get token:**
   - Click `POST /api/auth/login/`
   - Click "Try it out"
   - Enter credentials and click "Execute"
   - **Copy the `access` token from response**
4. **Authorize:**
   - Click "Authorize" button (lock icon)
   - Enter: `Bearer <your-access-token>`
   - Click "Authorize"
5. **Test protected endpoints:**
   - Try `GET /api/auth/me/` to see your user data

## What's Included

### 🔐 Authentication System
- User Registration (inactive by default)
- Account Activation (email-based)
- JWT Login/Logout
- Password Reset (email-based)
- Current User Profile
- Token Refresh

### 📁 File Structure
```
api/
├── authentication/     # Complete auth domain
│   ├── apis.py        # API endpoints
│   ├── services.py    # Business logic
│   ├── selectors.py   # Data retrieval
│   ├── serializers.py # Input/output serialization
│   ├── tokens.py      # Token generation/validation
│   ├── emails.py      # Plain text email sending
│   ├── urls.py        # URL routing
│   └── tests/         # Comprehensive tests
├── common/            # Shared utilities
│   ├── exceptions.py       # Custom exceptions
│   └── exception_handler.py # DRF exception handler
├── models.py          # CustomUser model
├── permissions.py     # Role-based permissions
└── urls.py           # Main URL routing

dvdrental_project/
├── settings.py        # Django configuration
└── urls.py           # Main URL routing

docker-compose.yml    # PostgreSQL + Django
Dockerfile           # Django container
entrypoint.sh        # Startup script
requirements.txt     # Python dependencies
```

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/auth/register/` | Register new user |
| POST | `/api/auth/activate/` | Activate user account |
| POST | `/api/auth/login/` | Login user |
| GET | `/api/auth/me/` | Get current user |
| POST | `/api/auth/password-reset/` | Request password reset |
| POST | `/api/auth/password-reset/confirm/` | Confirm password reset |
| POST | `/api/auth/token/refresh/` | Refresh JWT token |

## Testing

Import the Postman collection:
- `DVD_Rental_Auth_API.postman_collection.json`
- `DVD_Rental_Auth_Environment.postman_environment.json`

## Features

- ✅ JWT Authentication
- ✅ Email-based activation
- ✅ Password reset flow
- ✅ Role-based permissions
- ✅ Comprehensive error handling
- ✅ Plain text emails (no templates)
- ✅ Docker containerization
- ✅ PostgreSQL database
- ✅ Swagger documentation
- ✅ Complete test coverage

Ready for step-by-step feature additions! 🚀

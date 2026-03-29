# PetFeeder Backend

This is the Django REST Framework backend for the PetFeeder application.

## Features

- User authentication and registration
- Pet management
- Device management
- Feeding schedules
- Feeding logs

## Setup

1. Clone the repository
2. Create a virtual environment: `python -m venv venv`
3. Activate the virtual environment: `venv\Scripts\activate` (Windows)
4. Install dependencies: `pip install -r requirements.txt`
5. Run migrations: `python manage.py migrate`
6. Create superuser: `python manage.py createsuperuser`
7. Run the server: `python manage.py runserver`

## API Endpoints

- `/api/auth/` - Authentication (POST with username and password)
- `/api/users/` - User management
- `/api/pets/` - Pet management
- `/api/devices/` - Device management
- `/api/schedules/` - Feeding schedules
- `/api/logs/` - Feeding logs

## Testing

Use httpie to test endpoints:

```bash
http POST http://127.0.0.1:8000/api/auth/ username=admin password=password123
http GET http://127.0.0.1:8000/api/pets/ "Authorization: Token <token>"
```
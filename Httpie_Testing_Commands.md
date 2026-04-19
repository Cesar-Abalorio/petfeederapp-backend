# Httpie Testing Commands for PetFeeder API Demo

## Setup
Make sure the backend server is running:
```bash
cd "d:\School Projects\App_Dev\PetFeedApp\petfeederapp-backend"
python manage.py runserver
```

## 1. User Registration
**Purpose**: Create a new user account
```bash
http POST http://127.0.0.1:8000/api/register/ username=demo_user password=DemoPass123 email=demo@example.com
```

## 2. User Authentication (Login)
**Purpose**: Get authentication token for API access
```bash
http POST http://127.0.0.1:8000/api/auth/ username=demo_user password=DemoPass123
```
*Note: Save the token from the response for subsequent requests*

## 3. Get User Profile
**Purpose**: Retrieve current user profile information
```bash
http GET http://127.0.0.1:8000/api/profile/ "Authorization: Token YOUR_TOKEN_HERE"
```

## 4. List Devices
**Purpose**: Get all devices owned by the authenticated user
```bash
http GET http://127.0.0.1:8000/api/devices/ "Authorization: Token YOUR_TOKEN_HERE"
```

## 5. Create a Device
**Purpose**: Add a new pet feeder device
```bash
http POST http://127.0.0.1:8000/api/devices/ "Authorization: Token YOUR_TOKEN_HERE" name="Living Room Feeder" location="Living Room" status="active"
```

## 6. Scan for Devices
**Purpose**: Discover available devices on the network
```bash
http GET http://127.0.0.1:8000/api/devices/scan/ "Authorization: Token YOUR_TOKEN_HERE"
```

## 7. List Pets
**Purpose**: Get all pets owned by the authenticated user
```bash
http GET http://127.0.0.1:8000/api/pets/ "Authorization: Token YOUR_TOKEN_HERE"
```

## 8. Create a Pet
**Purpose**: Add a new pet to the system
```bash
http POST http://127.0.0.1:8000/api/pets/ "Authorization: Token YOUR_TOKEN_HERE" name="Fluffy" breed="Golden Retriever" age=3 weight=30.5
```

## 9. List Feeding Schedules
**Purpose**: Get all feeding schedules for user's devices
```bash
http GET http://127.0.0.1:8000/api/schedules/ "Authorization: Token YOUR_TOKEN_HERE"
```

## 10. Create a Feeding Schedule
**Purpose**: Set up an automated feeding schedule
```bash
http POST http://127.0.0.1:8000/api/schedules/ "Authorization: Token YOUR_TOKEN_HERE" pet_id=1 device_id=1 time="08:00:00" amount=100 recurring:=true
```

## 11. List Feeding Logs
**Purpose**: View feeding history and logs
```bash
http GET http://127.0.0.1:8000/api/logs/ "Authorization: Token YOUR_TOKEN_HERE"
```

## 12. Manual Device Feeding
**Purpose**: Trigger immediate feeding from a device
```bash
http POST http://127.0.0.1:8000/api/devices/feed/ "Authorization: Token YOUR_TOKEN_HERE" device_id=1 amount=50
```

## 13. User Logout
**Purpose**: Invalidate the current authentication token
```bash
http POST http://127.0.0.1:8000/api/auth/logout/ "Authorization: Token YOUR_TOKEN_HERE"
```

## Demo Flow Sequence
1. **Register** → Get user account
2. **Login** → Get token
3. **Create Device** → Add feeder hardware
4. **Create Pet** → Add pet info
5. **Create Schedule** → Set feeding times
6. **Manual Feed** → Test immediate feeding
7. **View Logs** → Check feeding history
8. **Logout** → End session

## Error Testing Examples
**Invalid Login** (should return 401):
```bash
http POST http://127.0.0.1:8000/api/auth/ username=wrong password=wrong
```

**Unauthorized Access** (should return 401):
```bash
http GET http://127.0.0.1:8000/api/devices/
```

**Invalid Data** (should return 400):
```bash
http POST http://127.0.0.1:8000/api/pets/ "Authorization: Token YOUR_TOKEN_HERE" name=""
```
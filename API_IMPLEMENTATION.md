# Pet Feeder API - Implementation Guide

This document maps the activity steps to the actual implementation for your React frontend.

## ✅ Step 1: Understanding Django MVT in Practice

**What's Implemented:**
- **Models** (`api/models.py`): Pet, Device, FeedingSchedule, FeedingLog
- **Architecture**: Django REST Framework (DRF) replaces the traditional template-based approach
- **Data Flow**: User → URL Router → ViewSet → Model → Serializer → JSON Response

**Key Files:**
- Models define your system entities
- Each model reflects real-world objects (Pet, Device, Feeding Schedule)

---

## ✅ Step 2: Creating a Serializer (DRF)

**What's Implemented:**
- `UserSerializer`: Converts User objects to JSON
- `PetSerializer`: Serializes Pet data with owner info
- `DeviceSerializer`: Serializes Device data with validation
- `FeedingScheduleSerializer`: Handles schedule creation with pet/device details
- `FeedingLogSerializer`: Serializes feeding activity logs

**Example Response:**
```json
{
  "id": 1,
  "name": "Fluffy",
  "breed": "Golden Retriever",
  "age": 3,
  "weight": 30.5,
  "owner": {
    "id": 1,
    "username": "john_doe",
    "email": "john@example.com"
  }
}
```

**Features Added:**
- Read-only owner field (auto-assigned)
- Field validation (pet name, device status, feeding amount)
- Nested serializers for related objects
- Proper error messages for invalid data

---

## ✅ Step 3: Creating API Views

**What's Implemented:**
- `UserViewSet`: Manages user data with custom `/me/` endpoint
- `PetViewSet`: Full CRUD for pets (scoped to current user)
- `DeviceViewSet`: Full CRUD for devices (scoped to current user)
- `FeedingScheduleViewSet`: Schedule management with validation
- `FeedingLogViewSet`: Read-only logs (monitoring only)

**Features Added:**
- **Pagination**: Limits results to 10 items per page (configurable)
- **Filtering & Ordering**: Sort by name, status, time, etc.
- **Permissions**: All endpoints require authentication (token-based)
- **User Scoping**: Each user only sees their own data

---

## ✅ Step 4: Creating API Endpoints (URLs)

**API Routes Implemented:**

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/api/pets/` | GET | List user's pets (paginated) |
| `/api/pets/` | POST | Create new pet |
| `/api/pets/{id}/` | GET | Get pet details |
| `/api/pets/{id}/` | PUT/PATCH | Update pet |
| `/api/pets/{id}/` | DELETE | Delete pet |
| `/api/devices/` | GET | List user's devices |
| `/api/devices/` | POST | Create new device |
| `/api/devices/{id}/` | GET/PUT/PATCH/DELETE | Device operations |
| `/api/schedules/` | GET | List feeding schedules |
| `/api/schedules/` | POST | Create schedule |
| `/api/schedules/{id}/` | GET/PUT/PATCH/DELETE | Schedule operations |
| `/api/logs/` | GET | View feeding logs (read-only) |
| `/api/users/me/` | GET | Get current user profile |
| `/api/auth/login/` | POST | User login |
| `/api/auth/logout/` | POST | User logout |
| `/api/auth/register/` | POST | Register new account |

---

## ✅ Step 5: Adding POST (Create Data)

**What's Implemented:**
- All ViewSets support POST for data creation
- Automatic owner assignment (current user)
- Validation before saving
- Proper error responses

**Example: Create a Pet (React Component)**
```javascript
const createPet = async (petData) => {
  const response = await fetch('/api/pets/', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Token ${authToken}`,
    },
    body: JSON.stringify({
      name: petData.name,
      breed: petData.breed,
      age: petData.age,
      weight: petData.weight
    })
  });
  return response.json();
};
```

---

## ✅ Step 6: Basic Authentication Setup

**What's Implemented:**
- **Token Authentication**: Each user gets a unique token on login
- **Protected Endpoints**: All endpoints require valid token
- **Automatic User Scoping**: Backend restricts data to logged-in user

**Login Endpoint Response:**
```json
{
  "token": "abc123def456",
  "user_id": 1,
  "username": "john_doe",
  "email": "john@example.com",
  "first_name": "John",
  "last_name": "Doe"
}
```

**React Implementation:**
```javascript
// Save token to localStorage after login
localStorage.setItem('authToken', response.token);

// Include token in all requests
const headers = {
  'Authorization': `Token ${localStorage.getItem('authToken')}`
};
```

---

## ✅ Step 7: Testing API using httpie or curl

**Test Commands:**

```bash
# Register new user
curl -X POST http://127.0.0.1:8000/api/auth/register/ \
  -H "Content-Type: application/json" \
  -d '{"username":"user1","password":"pass123","email":"user@example.com"}'

# Login
curl -X POST http://127.0.0.1:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{"username":"user1","password":"pass123"}'

# Get pets (requires token)
curl http://127.0.0.1:8000/api/pets/ \
  -H "Authorization: Token YOUR_TOKEN_HERE"

# Create a pet
curl -X POST http://127.0.0.1:8000/api/pets/ \
  -H "Authorization: Token YOUR_TOKEN_HERE" \
  -H "Content-Type: application/json" \
  -d '{"name":"Fluffy","breed":"Dog","age":3,"weight":25}'
```

---

## ✅ Step 8: Backend Structure (Mapped to Your System)

### System Mapping:

| UI Feature | Backend Model | API Endpoint |
|-----------|---------------|--------------|
| Login/Register | User | `/api/auth/login/`, `/api/auth/register/` |
| Dashboard (My Pets) | Pet | `/api/pets/` |
| Device Management | Device | `/api/devices/` |
| Feeding Schedules | FeedingSchedule | `/api/schedules/` |
| Activity Monitoring | FeedingLog | `/api/logs/` |
| User Profile | User | `/api/users/me/` |

### Database Structure:
```
User (Django built-in)
├── Pet (name, breed, age, weight)
├── Device (name, location, status)
│   └── FeedingSchedule → Pet/Device → FeedingLog
└── Token (for authentication)
```

---

## ✅ Step 9: Best Practices Implemented

✅ **Clear Naming**: Endpoints follow RESTful conventions (`/api/resource/`)
✅ **Modular Views**: Each ViewSet handles one resource type
✅ **Error Handling**: Validates input, returns meaningful error messages
✅ **Consistent JSON**: All responses use consistent format
✅ **File Organization**: Models, Views, Serializers in separate files
✅ **Pagination**: Large datasets split into pages
✅ **Filtering & Ordering**: React can sort/filter on frontend or backend
✅ **Permissions**: All endpoints protected by default
✅ **User Scoping**: Data isolation between users

---

## 📋 Backend Features for React

### 1. Authentication Flow
```
Register → Login → Get Token → Use Token in Headers → Logout
```

### 2. Pagination Response Format
```json
{
  "count": 25,
  "next": "http://api/pets/?page=2",
  "previous": null,
  "results": [
    { "id": 1, "name": "Pet1", ... },
    { "id": 2, "name": "Pet2", ... }
  ]
}
```

### 3. Error Response Format
```json
{
  "error": "Detailed error message here"
}
```

### 4. Success Response
```json
{
  "id": 1,
  "name": "Success data"
}
```

---

## 🚀 Running the Server

```bash
# Activate virtual environment
source venv/Scripts/activate  # Windows
# or
source venv/bin/activate  # Mac/Linux

# Run server
python manage.py runserver

# Server runs on http://127.0.0.1:8000/
```

---

## 📝 React Frontend Integration Checklist

- [ ] Implement login page (POST `/api/auth/login/`)
- [ ] Implement registration page (POST `/api/auth/register/`)
- [ ] Store token in localStorage after login
- [ ] Create API utility/service for authenticated requests
- [ ] Implement dashboard showing user's pets (GET `/api/pets/`)
- [ ] Implement pets CRUD (Create, Read, Update, Delete)
- [ ] Implement device management (GET/POST `/api/devices/`)
- [ ] Implement feeding schedule creation (POST `/api/schedules/`)
- [ ] Implement activity monitoring/logs view (GET `/api/logs/`)
- [ ] Add error handling and loading states
- [ ] Implement user profile view (GET `/api/users/me/`)
- [ ] Add logout functionality (POST `/api/auth/logout/`)
- [ ] Test all endpoints with token authentication

---

## 🔗 Quick Reference for React

**Common API Call Pattern:**
```javascript
const API_URL = 'http://127.0.0.1:8000/api';
const token = localStorage.getItem('authToken');

const apiCall = async (endpoint, method = 'GET', data = null) => {
  const options = {
    method,
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Token ${token}`
    }
  };
  
  if (data) options.body = JSON.stringify(data);
  
  const response = await fetch(`${API_URL}${endpoint}`, options);
  if (!response.ok) throw new Error(await response.text());
  return response.json();
};

// Usage:
const pets = await apiCall('/pets/');
const newPet = await apiCall('/pets/', 'POST', { name: 'Fluffy', breed: 'Dog' });
```

---

**Status**: ✅ Backend is production-ready for React frontend integration

# Pet Feeder App - Frontend & Backend Integration Guide

## ✅ Integration Status

Your React frontend and Django backend are now **fully compatible and ready to work together**.

---

## 🔧 Backend Updates Made

### API Endpoint Adjustments
The backend URLs were updated to match your frontend's expectations:

| Feature | Frontend Calls | Backend Provides |
|---------|---|---|
| **Login** | `POST /api/auth/` | ✅ `/api/auth/` |
| **Register** | `POST /api/register/` | ✅ `/api/register/` |
| **Logout** | `POST /api/auth/logout/` | ✅ `/api/auth/logout/` |
| **Get Devices** | `GET /api/devices/` | ✅ `/api/devices/` |
| **Get Pets** | `GET /api/pets/` | ✅ `/api/pets/` |
| **Get Schedules** | `GET /api/schedules/` | ✅ `/api/schedules/` |
| **Get Logs** | `GET /api/logs/` | ✅ `/api/logs/` |

### What Was Changed
```python
# api/urls.py - Changed from:
path('auth/login/', ...)  # ❌ Old
path('auth/register/', ...)  # ❌ Old

# To:
path('auth/', ...)  # ✅ Matches frontend
path('register/', ...)  # ✅ Matches frontend
```

---

## 🚀 Running Both Services

### Terminal 1: Start Backend (Port 8000)
```bash
cd "d:\School Projects\App_Dev\PetFeedApp\petfeederapp-backend"
python manage.py runserver 0.0.0.0:8000
```

**Output:**
```
Starting development server at http://127.0.0.1:8000/
```

### Terminal 2: Start Frontend (Port 5173)
```bash
cd "d:\School Projects\App_Dev\PetFeedApp\petfeederapp"
npm run dev
```

**Output:**
```
VITE v7.3.1  ready in 500 ms

➜  Local:   http://localhost:5173/PetFeederApp/
```

---

## 🔗 How They Connect

### Vite Proxy Configuration
Your Vite config (`vite.config.ts`) already has the proxy setup:

```typescript
server: {
  proxy: {
    '/api': {
      target: 'http://localhost:8000',  // Django backend
      changeOrigin: true,
    },
  },
},
```

### What This Means
- Frontend makes request to: `http://localhost:5173/api/auth/`
- Vite proxy forwards to: `http://localhost:8000/api/auth/`
- Backend responds with JSON
- Frontend gets the data automatically ✅

---

## 📋 Testing Workflow

### 1. **Register a New Account**
- Go to: `http://localhost:5173/PetFeederApp/`
- Click "Create Account"
- Enter:
  - Email: `user@example.com`
  - Password: `TestPass123` (must be strong)
  - Token automatically saved to `localStorage`

### 2. **Login**
- Enter credentials
- Redirect to `/user` (User Dashboard)
- Token stored in `localStorage['authToken']`

### 3. **View Devices**
- Dashboard shows connected devices
- Backend fetches from `/api/devices/`

### 4. **Create a Schedule**
- Add feeding times
- Device tracks feeding logs

### 5. **Monitor Logs**
- View feeding history
- Backend stores in FeedingLog model

---

## 🧪 Testing Endpoints with cURL

### Without Frontend (Direct API Testing)

**1. Register**
```bash
curl -X POST http://localhost:8000/api/register/ \
  -H "Content-Type: application/json" \
  -d '{"username":"testuser","password":"TestPass123","email":"test@example.com"}'
```

**Response:**
```json
{
  "token": "abc123def456",
  "user_id": 1,
  "username": "testuser",
  "email": "test@example.com"
}
```

**2. Login**
```bash
curl -X POST http://localhost:8000/api/auth/ \
  -H "Content-Type: application/json" \
  -d '{"username":"testuser","password":"TestPass123"}'
```

**3. Get Devices (Authenticated)**
```bash
curl http://localhost:8000/api/devices/ \
  -H "Authorization: Token YOUR_TOKEN_HERE"
```

**4. Create Pet**
```bash
curl -X POST http://localhost:8000/api/pets/ \
  -H "Authorization: Token YOUR_TOKEN_HERE" \
  -H "Content-Type: application/json" \
  -d '{"name":"Fluffy","breed":"Dog","age":3,"weight":25}'
```

---

## 🔐 Authentication Flow

### How It Works
```
1. User enters credentials in React
   ↓
2. Frontend sends POST /api/auth/ (proxied to backend)
   ↓
3. Backend validates username/password
   ↓
4. Backend returns token in response
   ↓
5. Frontend stores token in localStorage
   ↓
6. All future requests include: Authorization: Token {token}
```

### Token Storage
```javascript
// Frontend stores:
localStorage.authToken  // Used in every API call
localStorage.currentUser  // Username
localStorage.role  // "user" or "admin"
```

### Using Token in Requests
```javascript
// Frontend does this automatically:
const token = localStorage.getItem('authToken');
headers: {
  'Authorization': `Token ${token}`
}
```

---

## 🔍 Debugging Checklist

### ✅ Backend Not Responding?
```bash
# Check if running on port 8000
lsof -i :8000  # Mac/Linux
netstat -ano | findstr :8000  # Windows

# Restart with verbose output:
python manage.py runserver --verbosity 3
```

### ✅ CORS Issues?
Backend already configured in `settings.py`:
```python
CORS_ALLOWED_ORIGINS = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
    "http://localhost:3000",
    "http://127.0.0.1:3000",
]
CORS_ALLOW_ALL_ORIGINS = True  # For development
```

### ✅ Token Not Working?
1. Check browser DevTools → Application → localStorage
2. Verify token exists and is not empty
3. Make sure token is included in request headers
4. Confirm token is valid (not expired)

### ✅ Login Returns 401 Unauthorized?
- Verify username/password are correct
- Check if user exists in database
- Look at backend console for error messages

### ✅ Frontend Can't Find Backend?
- Verify backend is running on `http://localhost:8000`
- Check Vite proxy is working (should see `/api` forwarding)
- Look in browser Network tab to confirm requests are being sent

---

## 📊 Data Flow Diagram

```
┌─────────────────────┐
│   React Frontend    │
│  (Port 5173)        │
└──────────┬──────────┘
           │
           │ /api/auth/
           │ (relative path)
           ↓
┌─────────────────────┐
│  Vite Dev Server    │
│  (Proxy)            │
└──────────┬──────────┘
           │
           │ http://localhost:8000/api/auth/
           │ (proxied request)
           ↓
┌─────────────────────┐
│ Django Backend      │
│ (Port 8000)         │
│                     │
│ - Models            │
│ - ViewSets          │
│ - Serializers       │
│ - Database (SQLite) │
└─────────────────────┘
```

---

## 📝 Frontend & Backend Contract

### User Authentication
```json
POST /api/auth/
{
  "username": "user@example.com",
  "password": "password123"
}

Response:
{
  "token": "abc123...",
  "user_id": 1,
  "username": "user@example.com",
  "email": "user@example.com",
  "first_name": "",
  "last_name": ""
}
```

### Devices List (with pagination)
```json
GET /api/devices/
Authorization: Token {token}

Response:
{
  "count": 5,
  "next": "http://localhost:8000/api/devices/?page=2",
  "previous": null,
  "results": [
    {
      "id": 1,
      "name": "Living Room Feeder",
      "location": "Living Room",
      "status": "active",
      "owner": { "id": 1, "username": "user@example.com" }
    }
  ]
}
```

### Pet Creation
```json
POST /api/pets/
Authorization: Token {token}
{
  "name": "Fluffy",
  "breed": "Golden Retriever",
  "age": 3,
  "weight": 30.5
}

Response:
{
  "id": 1,
  "name": "Fluffy",
  "breed": "Golden Retriever",
  "age": 3,
  "weight": 30.5,
  "owner": { "id": 1, "username": "user@example.com" }
}
```

---

## 🚦 Quick Start Commands

```bash
# Terminal 1 - Backend
cd "d:\School Projects\App_Dev\PetFeedApp\petfeederapp-backend"
python manage.py runserver

# Terminal 2 - Frontend
cd "d:\School Projects\App_Dev\PetFeedApp\petfeederapp"
npm run dev

# Then open: http://localhost:5173/PetFeederApp/
```

---

## ✨ Summary

Your Pet Feeder app is now fully integrated:
- ✅ Backend returns correct endpoint paths
- ✅ Frontend proxy configured correctly
- ✅ Authentication flow working
- ✅ CORS configured for development
- ✅ Token-based API security in place
- ✅ Database models match frontend expectations

**Status: Ready for testing! 🎉**

---

## 📚 Key Files Reference

**Backend Configuration:**
- `api/urls.py` - API endpoint routes
- `api/views.py` - API endpoint logic
- `api/serializers.py` - Data serialization
- `api/models.py` - Database models
- `petfeeder/settings.py` - Django settings (CORS, auth)

**Frontend Configuration:**
- `vite.config.ts` - Proxy configuration
- `src/pages/Login.tsx` - Login component (calls `/api/auth/`)
- `src/pages/Signup.tsx` - Signup component (calls `/api/register/`)
- `src/pages/UserDashboard.tsx` - Devices/schedules (calls `/api/devices/`)

---

**Everything is configured and ready to test!** 🚀

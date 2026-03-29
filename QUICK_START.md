# Quick Start - Frontend & Backend Testing

## 🎯 Setup (One Time Only)

### Backend
```bash
cd "d:\School Projects\App_Dev\PetFeedApp\petfeederapp-backend"
python -m venv venv  # If not already created
venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
```

### Frontend
```bash
cd "d:\School Projects\App_Dev\PetFeedApp\petfeederapp"
npm install  # If not already done
```

---

## ▶️ Running the App (Every Time)

### Start Backend (Terminal 1)
```bash
cd "d:\School Projects\App_Dev\PetFeedApp\petfeederapp-backend"
python manage.py runserver
```
✅ Should see: `Starting development server at http://127.0.0.1:8000/`

### Start Frontend (Terminal 2)
```bash
cd "d:\School Projects\App_Dev\PetFeedApp\petfeederapp"
npm run dev
```
✅ Should see: `Local: http://localhost:5173/PetFeederApp/`

---

## 🧪 Testing Steps

### 1. Register
- Open: `http://localhost:5173/PetFeederApp/`
- Click "Create Account"
- Enter:
  - Email: `testuser@example.com`
  - Password: `TestPass123`
  - Confirm: `TestPass123`
- ✅ Should redirect to login

### 2. Login
- Enter credentials from above
- ✅ Should redirect to `/user` dashboard

### 3. Check Token
- Press F12 → Application → Local Storage
- ✅ Should see `authToken` (long string)

### 4. View Devices
- Dashboard should show devices from backend
- ✅ Devices loaded from `/api/devices/`

### 5. Create Schedule
- Add feeding time
- Select device
- ✅ Should save and appear in list

### 6. Check Logs
- Click on logs/activity
- ✅ Should show feeding history

---

## 🔧 Troubleshooting

### "Cannot reach backend"
```bash
# Check backend is running:
curl http://localhost:8000/api/auth/
# Should get error (requires credentials), not "Connection refused"
```

### "CORS Error"
- Backend settings already configured ✅
- If error persists, ensure backend is running on `localhost:8000`

### "Invalid Token"
- Clear localStorage: F12 → Application → Local Storage → Delete all
- Login again fresh

### "401 Unauthorized on API calls"
- Check token is in localStorage
- Verify you're logged in first

---

## 📊 API Endpoints

All endpoints require `Authorization: Token {token}` header (except login/register)

```
POST   /api/auth/              - Login
POST   /api/register/          - Register
POST   /api/auth/logout/       - Logout

GET    /api/pets/              - List pets
POST   /api/pets/              - Create pet
GET/PUT/DELETE /api/pets/{id}/ - Pet operations

GET    /api/devices/           - List devices
GET    /api/schedules/         - List schedules
GET    /api/logs/              - View feeding logs
```

---

## ✅ Success Indicators

- [ ] Backend runs without errors
- [ ] Frontend starts and loads on port 5173
- [ ] Can register new account
- [ ] Can login with credentials
- [ ] Token saved in localStorage
- [ ] Dashboard shows devices
- [ ] Can create schedules
- [ ] Can view logs
- [ ] No browser console errors

---

## 🚀 Status: READY TO TEST
All integration issues resolved. Both apps working together!

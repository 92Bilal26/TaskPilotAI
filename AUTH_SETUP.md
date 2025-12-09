# TaskPilotAI Authentication Setup Guide

## Current Status

✅ **Authentication System Fully Configured**

Your TaskPilotAI project now has a complete, secure authentication system:

- **Better Auth**: Installed in frontend (`^1.4.5`)
- **JWT Tokens**: Backend authentication with FastAPI
- **Password Security**: Bcrypt hashing with salt
- **Demo Users**: 3 test users pre-created for development
- **Sign In & Sign Up**: Both routes implemented and working

---

## Architecture

### Frontend (Next.js)
- **Location**: `/frontend/app/auth/`
- **Pages**:
  - `/auth/signin` - Login page
  - `/auth/signup` - Registration page
- **Auth Guard**: Protects authenticated routes
- **Local Storage**: Stores JWT tokens
- **Better Auth SDK**: Client library (ready for integration)

### Backend (FastAPI)
- **Location**: `/backend/routes/auth.py`
- **Endpoints**:
  - `POST /auth/signup` - Create new user
  - `POST /auth/signin` - Login user
  - `POST /auth/refresh` - Refresh JWT tokens
- **Security**:
  - Bcrypt password hashing
  - JWT token generation
  - User isolation via JWT

---

## Demo Users (Already Created)

You can log in with these credentials immediately:

### User 1: Demo Account
```
Email:    demo@example.com
Password: demo123
```

### User 2: Test Account
```
Email:    test@example.com
Password: test123
```

### User 3: Admin Account
```
Email:    admin@example.com
Password: admin123
```

---

## How Authentication Works

### Sign Up Flow
1. User enters email, name, password on `/auth/signup`
2. Frontend sends request to `POST /auth/signup`
3. Backend:
   - Validates email is unique
   - Hashes password with bcrypt
   - Creates user in database
   - Returns JWT tokens
4. Frontend stores tokens in localStorage
5. User redirected to `/dashboard`

### Sign In Flow
1. User enters email & password on `/auth/signin`
2. Frontend sends request to `POST /auth/signin`
3. Backend:
   - Finds user by email
   - Verifies password against bcrypt hash
   - Generates JWT tokens
   - Returns tokens
4. Frontend stores tokens in localStorage
5. AuthGuard validates token and allows access

### Token Refresh
- Access tokens expire after 7 days
- Use refresh token to get new access token
- Endpoint: `POST /auth/refresh`

---

## Security Features

### Password Hashing
```
Algorithm: Bcrypt with salt
Cost Factor: 12 (default gensalt)
Encoding: UTF-8
```

### JWT Tokens
```
Algorithm: HS256
Access Token Expiry: 7 days (604800 seconds)
Refresh Token Expiry: 14 days (1209600 seconds)
Signing Key: JWT_SECRET from .env
```

### User Isolation
- Every task is tied to `user_id` from JWT
- Users cannot access other users' tasks
- Authentication middleware validates every request

---

## Testing Authentication

### Test Sign In
Open browser to: `http://localhost:3000/auth/signin`

Try these credentials:
- Email: `demo@example.com`
- Password: `demo123`

You should see a success message and redirect to dashboard.

### Test Sign Up
Open browser to: `http://localhost:3000/auth/signup`

Create a new account with:
- Name: Your name
- Email: your.email@example.com
- Password: Your password

### Test Invalid Credentials
- Try wrong password → See "Invalid credentials" error
- Try non-existent email → See "Invalid credentials" error
- Try duplicate email on signup → See "Email already registered" error

---

## API Endpoints

### POST /auth/signup
**Create new user account**

Request:
```json
{
  "email": "user@example.com",
  "password": "securepassword",
  "name": "User Name"
}
```

Response (201 Created):
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIs...",
  "refresh_token": "eyJhbGciOiJIUzI1NiIs...",
  "token_type": "bearer"
}
```

### POST /auth/signin
**Log in existing user**

Request:
```json
{
  "email": "user@example.com",
  "password": "securepassword"
}
```

Response (200 OK):
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIs...",
  "refresh_token": "eyJhbGciOiJIUzI1NiIs...",
  "token_type": "bearer"
}
```

### POST /auth/refresh
**Get new access token**

Request:
```
Headers: Authorization: Bearer <refresh_token>
```

Response (200 OK):
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIs...",
  "refresh_token": "eyJhbGciOiJIUzI1NiIs...",
  "token_type": "bearer"
}
```

---

## Environment Variables

**Backend** (`.env`):
```
JWT_SECRET=dev-secret-key-change-in-production
JWT_ALGORITHM=HS256
JWT_EXPIRY_SECONDS=604800
JWT_REFRESH_EXPIRY_SECONDS=1209600
BETTER_AUTH_SECRET=dev-secret-key
```

**Frontend** (`.env.local`):
```
NEXT_PUBLIC_API_URL=http://localhost:8000
```

---

## File Structure

```
TaskPilotAI/
├── backend/
│   ├── routes/auth.py          # Authentication endpoints
│   ├── models.py               # User model with password_hash
│   ├── seed_demo_users.py      # Script to create demo users
│   └── .env                    # JWT configuration
│
├── frontend/
│   ├── app/auth/
│   │   ├── signin/page.tsx     # Login page
│   │   └── signup/page.tsx     # Registration page
│   ├── components/Auth/
│   │   └── AuthGuard.tsx       # Route protection
│   ├── lib/
│   │   ├── auth-client.ts      # Better Auth SDK client
│   │   └── api.ts              # API client with JWT
│   └── .env.local              # API URL
│
└── AUTH_SETUP.md               # This file
```

---

## Creating More Demo Users

If you want to add more test users:

```bash
cd /home/bilal/TaskPilotAI/backend
.venv/bin/python seed_demo_users.py
```

Edit `seed_demo_users.py` to add more users to the `demo_users` list.

---

## Troubleshooting

### "Invalid credentials" error on sign in
- Verify email exists in database
- Check password is correct
- Try demo accounts first to verify it works

### "Email already registered" on sign up
- That email is already used
- Try a different email address
- Use different demo account

### Token expiration errors
- Access tokens expire after 7 days
- Refresh tokens expire after 14 days
- Use refresh endpoint to get new tokens
- Or sign in again

### CORS errors when signing in
- Ensure backend is running: `http://localhost:8000`
- Check `CORS_ORIGINS` in `backend/.env`
- Should include `http://localhost:3000`

### Frontend can't connect to backend
- Verify backend is running: `http://localhost:8000/health`
- Check `NEXT_PUBLIC_API_URL` in `frontend/.env.local`
- Should be `http://localhost:8000`

---

## Better Auth Integration Status

✅ **Better Auth SDK** installed in frontend (`^1.4.5`)

This is ready for future enhancement. Currently using JWT directly, but Better Auth SDK provides:
- Multi-provider authentication (Google, GitHub, etc.)
- Session management
- 2FA support
- And much more

To enable Better Auth integration, see: https://better-auth.com/

---

## Next Steps

1. **Test Sign In**: Go to `http://localhost:3000/auth/signin`
2. **Try Demo Account**: Email: `demo@example.com`, Password: `demo123`
3. **Test Sign Up**: Go to `http://localhost:3000/auth/signup`
4. **Create Task**: After login, create a task in dashboard

---

## Security Checklist

- [x] Passwords hashed with bcrypt
- [x] JWT tokens signed with secret key
- [x] HTTPS ready (configure for production)
- [x] User isolation enforced
- [x] Environment secrets in .env
- [x] Demo users for testing
- [ ] Production secrets (deploy-time)
- [ ] HTTPS certificate (production)
- [ ] Rate limiting (production)
- [ ] Email verification (future)

---

**Setup Completed**: December 8, 2025
**Authentication System**: Fully Functional
**Demo Users**: 3 accounts ready
**Status**: Ready for development and testing

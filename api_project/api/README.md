# API Authentication and Permissions Documentation

## Overview
This API uses Token Authentication to secure endpoints. Users must authenticate to access most endpoints, and certain actions require admin privileges.

## Authentication

### How to Obtain a Token
Send a POST request to `/api/api-token-auth/` with your credentials:

**Request:**
```bash
POST /api/api-token-auth/
Content-Type: application/json

{
    "username": "your_username",
    "password": "your_password"
}
```

**Response:**
```json
{
    "token": "9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b"
}
```

### How to Use the Token
Include the token in the `Authorization` header of all subsequent requests:
```
Authorization: Token 9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b
```

**Example:**
```bash
curl http://127.0.0.1:8000/api/books_all/ \
  -H "Authorization: Token 9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b"
```

## Permissions

### Endpoint Permissions

| Endpoint | Method | Permission Required | Description |
|----------|--------|-------------------|-------------|
| `/api/books/` | GET | IsAuthenticated | List all books |
| `/api/books_all/` | GET | IsAuthenticated | List all books (ViewSet) |
| `/api/books_all/` | POST | IsAuthenticated | Create a new book |
| `/api/books_all/<id>/` | GET | IsAuthenticated | Retrieve a specific book |
| `/api/books_all/<id>/` | PUT/PATCH | IsAuthenticated | Update a book |
| `/api/books_all/<id>/` | DELETE | IsAdminUser | Delete a book (admin only) |

### Permission Classes Explained

- **IsAuthenticated**: User must provide a valid token
- **IsAdminUser**: User must be authenticated AND have `is_staff=True`

### Making a User an Admin

Use Django shell:
```python
from django.contrib.auth.models import User
user = User.objects.get(username='username')
user.is_staff = True
user.save()
```

Or through Django admin panel at `/admin/`

## Error Responses

### 401 Unauthorized
Token missing or invalid:
```json
{
    "detail": "Authentication credentials were not provided."
}
```

**Solution**: Include valid token in Authorization header

### 403 Forbidden
Insufficient permissions:
```json
{
    "detail": "You do not have permission to perform this action."
}
```

**Solution**: Action requires admin privileges

## Security Best Practices

1. **Keep tokens secret**: Treat tokens like passwords
2. **Use HTTPS in production**: Prevents token interception
3. **Token rotation**: Consider implementing token expiration
4. **Store tokens securely**: Never commit tokens to version control

## Testing

### Create a test user:
```bash
python manage.py createsuperuser
```

### Get token:
```bash
curl -X POST http://127.0.0.1:8000/api/api-token-auth/ \
  -H "Content-Type: application/json" \
  -d '{"username": "testuser", "password": "testpass123"}'
```

### Test authenticated endpoint:
```bash
curl http://127.0.0.1:8000/api/books_all/ \
  -H "Authorization: Token YOUR_TOKEN_HERE"
```
```

---

#### **Add Inline Documentation to Code**

The code we wrote in Step 3 already includes comprehensive docstrings. Here's a summary of what's documented:

**In `views.py`:**
- Each view class has a docstring explaining its purpose
- Permission requirements are clearly stated
- The `get_permissions()` method explains action-based permissions

**In `settings.py`:**
- Comments explain what each authentication class does
- Permission settings are documented

---

## Summary of What You've Built

Congratulations! You've implemented a **fully secured API** with:

### Authentication Features:
✅ **Token-based authentication**: Users get unique tokens  
✅ **Token endpoint**: `/api/api-token-auth/` for obtaining tokens  
✅ **Secure requests**: All API calls require authentication

### Permission Features:
✅ **Global protection**: All endpoints require authentication by default  
✅ **Role-based access**: Admin-only actions (like delete)  
✅ **Flexible permissions**: Different rules for different actions  
✅ **Proper error responses**: 401 for missing auth, 403 for insufficient permissions

### Security Flow:
```
1. User registers/creates account
2. User logs in → receives token
3. User includes token in API requests
4. Server validates token
5. Server checks permissions
6. Request allowed or denied
# MisFinanzas API - Frontend Endpoints Guide

This document summarizes all available endpoints for the frontend application (Mobile/Web). 

**Base URL**: `http://localhost:8000/api/v1` *(or your production URL)*

## Authentication (`/auth`)

All endpoints except `/auth/login` and `/auth/register` require a **Bearer Token** in the `Authorization` header.
*Example:* `Authorization: Bearer <your_jwt_token>`

| Method | Endpoint | Description |
|---|---|---|
| `POST` | `/auth/register` | Creates a new user. Returns user data and JWT token. |
| `POST` | `/auth/login` | Authenticates a user with email and password. Returns a JWT token. |
| `GET` | `/auth/me` | **[Auth]** Gets the currently logged-in user's profile based on the token. |

---

## Accounts (`/accounts`)

Accounts represent the user's financial containers (e.g., Cash, Bank, Digital Wallet). All endpoints require **Authentication**.

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/accounts` | Retrieves all accounts for the current user. |
| `POST` | `/accounts` | Creates a new account. Body requires `name`, `type`, and `balance`. |
| `PUT` | `/accounts/{account_id}` | Updates an existing account's details. |
| `DELETE` | `/accounts/{account_id}` | Deletes the specified account. |
| `POST` | `/accounts/{account_id}/recalculate-balance` | Recalculates the account's balance from all its movements (useful for data integrity). |

---

## Categories (`/categories`)

Categories are used to classify movements (Incomes/Expenses). All endpoints require **Authentication**.

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/categories` | Retrieves all global categories and user-specific categories. Can be filtered by type (income/expense). |
| `POST` | `/categories` | Creates a custom category for the user. |
| `PUT` | `/categories/{category_id}` | Updates a user-created category. |
| `DELETE` | `/categories/{category_id}` | Deletes a user-created category. |

---

## Movements (`/movements`)

Movements are the actual transactions (incomes or expenses) applied to accounts. All endpoints require **Authentication**.

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/movements` | Retrieves all movements. Supports optional filters (date, account, category, type). |
| `GET` | `/movements/{movement_id}` | Retrieves details of a specific movement. |
| `POST` | `/movements` | Creates a new movement (adds/deducts balance from the associated account automatically). |
| `PUT` | `/movements/{movement_id}` | Updates a movement (automatically adjusts account balance). |
| `DELETE` | `/movements/{movement_id}` | Deletes a movement (automatically restores account balance). |

---

## Debts (`/debts`)

Debts represent money owed to or by the user. All endpoints require **Authentication**.

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/debts` | Retrieves all debts. Supports optional filters (status, type). |
| `GET` | `/debts/{debt_id}` | Retrieves details of a specific debt. |
| `POST` | `/debts` | Creates a new debt record (independent of movements initially). |
| `PUT` | `/debts/{debt_id}` | Updates a debt. Can be used to mark it as paid, optionally linking it to a movement. |
| `DELETE` | `/debts/{debt_id}` | Deletes a debt record. |

---

## How to use correctly in the Frontend (Axios / React Native / React)

### 1. Handling Authentication (Tokens)
When a user logs in via `POST /api/v1/auth/login`, save the `token` in your secure storage (e.g., `SecureStore` in Expo or `AsyncStorage`).

### 2. Setting up Axios Interceptor
Set up an Axios interceptor to automatically attach the token to every request so you don't have to pass it manually every time.

```javascript
import axios from 'axios';
import AsyncStorage from '@react-native-async-storage/async-storage';

const api = axios.create({
  baseURL: 'http://localhost:8000/api/v1',
});

api.interceptors.request.use(async (config) => {
  const token = await AsyncStorage.getItem('userToken');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

export default api;
```

### 3. Understanding the Response Format
Every successful request from this API wraps the main payload inside a `data` object.

For example, when fetching accounts (`GET /accounts`), the response looks like this:
```json
{
  "data": [
    { "id": 1, "name": "Cash", "balance": 100.5 },
    { "id": 2, "name": "Bank", "balance": 5000.0 }
  ]
}
```

**Frontend implementation example:**
```javascript
// Good ✅
const response = await api.get('/accounts');
const accounts = response.data.data; // Note the double .data (first is axios, second is API wrapper)
setAccounts(accounts);
```

### 4. Error Handling
The backend handles business logic errors using standard HTTP codes (`400`, `401`, `403`, `404`, `422`).
- `422 Unprocessable Entity`: You sent invalid data (e.g., missing a required field or wrong format).
- `401 Unauthorized`: Token is missing or expired.
- `403 Forbidden`: Trying to access a resource that belongs to another user.
- `404 Not Found`: Resource doesn't exist.

Handle these gracefully using try/catch blocks:
```javascript
try {
  await api.post('/accounts', { name: 'Savings', type: 'BANK', balance: 0 });
} catch (error) {
  if (error.response?.status === 422) {
    console.error("Validation Error:", error.response.data);
  } else if (error.response?.status === 401) {
    // Redirect to Login Screen
  }
}
```

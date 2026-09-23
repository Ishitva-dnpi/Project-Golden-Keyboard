# Operation Golden Keyboard — Backend API

Backend service built for the CSA inter-hostel coding competition, Operation Golden Keyboard. It tracks mission claiming, progress, completion status, points, and solver handles across campus hostels.

The project is built using Django and Django REST Framework (DRF), featuring five versions of the same Mission API to demonstrate different authentication mechanisms side by side.

---

## Project Structure

```
golden_keyboard/
├── manage.py
├── requirements.txt
├── README.md
├── mission_control/          # Core Django project settings and root routing
├── missions/                 # Mission model, serializer, admin, and test suite
│   ├── models.py
│   ├── serializers.py
│   ├── admin.py
│   ├── tests.py
│   └── management/commands/seed_demo.py
├── auth_none/                # Version 1: No Authentication
├── auth_basic/               # Version 2: HTTP Basic Authentication
├── auth_session/             # Version 3: Session Authentication
├── auth_token_scheme/        # Version 4: DRF Token Authentication
├── auth_jwt/                 # Version 5: SimpleJWT Authentication
└── postman/                  # Exported collection and environment files
```

All five API versions share the same `Mission` model and `MissionSerializer`. Only the authentication and permission classes (and custom auth views where needed) differ between the endpoints.

---

## Local Setup & Quickstart

### 1. Environment & Dependencies
```bash
# Create and activate virtual environment
python -m venv venv
# On Windows:
.\venv\Scripts\activate
# On Linux/macOS:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Database Migrations & Initial Data
```bash
python manage.py migrate

# Seed initial missions and demo user (player_one / hunter2pass)
python manage.py seed_demo

# Optional: Create an admin superuser to access /admin/
python manage.py createsuperuser
```

### 3. Run Tests
```bash
python manage.py test
```

### 4. Start the Server
```bash
python manage.py runserver
```

Once running, the base URL is `http://127.0.0.1:8000/`.

---

## API Endpoints

Each version provides full CRUD functionality (`GET`, `POST`, `GET /<id>/`, `PUT /<id>/`, `DELETE /<id>/`):

| Scheme | Base URL | Auth Helper Endpoints |
|---|---|---|
| **1. No Auth** | `/api/v1/no-auth/missions/` | None (Public access) |
| **2. Basic Auth** | `/api/v1/basic-auth/missions/` | Handled via HTTP headers |
| **3. Session Auth** | `/api/v1/session-auth/missions/` | `/api/v1/session-auth/login/`, `/api/v1/session-auth/logout/` |
| **4. Token Auth** | `/api/v1/token-auth/missions/` | `/api/v1/token-auth/login/` |
| **5. JWT Auth** | `/api/v1/jwt-auth/missions/` | `/api/v1/jwt-auth/login/`, `/api/v1/jwt-auth/refresh/` |

---

## Authentication Schemes Breakdown

### 1. No Authentication (`AllowAny`)
* **What is sent with requests:** Nothing. Standard HTTP requests with no auth headers or cookies.
* **Credentials & Expiry:** Not applicable since the endpoint is completely open.
* **Server State:** Stateless. The server performs no authentication checks or session lookups.
* **Verification:** Every incoming request is accepted immediately.
* **Tradeoffs:**
  * *Pros:* Very fast to test, zero configuration, works well for public read-only data.
  * *Cons:* No access control whatsoever. Anyone can create, edit, or delete competition data.

---

### 2. Basic Authentication (`HTTP Basic`)
* **What is sent with requests:** An HTTP header with Base64-encoded username and password:
  ```http
  Authorization: Basic cGxheWVyX29uZTpodW50ZXIycGFzcw==
  ```
* **Credentials & Expiry:** Does not expire automatically. Stays valid as long as the user's password remains unchanged.
* **Server State:** Stateless. The server stores no session data between requests; it verifies credentials against the database on each call.
* **Verification:** The server decodes the Base64 credentials from the header and authenticates the username and password against Django's user table.
* **Tradeoffs:**
  * *Pros:* Simple to set up, supported by almost every HTTP client, requires no token storage logic on the client.
  * *Cons:* Sends raw credentials on every single request. If not transmitted over HTTPS, credentials can be intercepted. Cannot be revoked without changing the password.

---

### 3. Session Authentication
* **What is sent with requests:** A session cookie (`sessionid`) sent automatically by the browser or HTTP client after logging in:
  ```http
  Cookie: sessionid=k8s3j9f...; csrftoken=...
  ```
* **Credentials & Expiry:** The user submits credentials once to `/login/`. The resulting session cookie expires according to Django's session configuration or when `/logout/` is called.
* **Server State:** Stateful. Django maintains session records in the database (`django_session` table) or cache.
* **Verification:** The server reads the session key from the cookie, queries the session store to find the corresponding user ID, and loads the user.
* **Tradeoffs:**
  * *Pros:* Well-suited for browser applications, easy to revoke sessions immediately from the server, credentials are not sent repeatedly.
  * *Cons:* Requires database or cache lookups for every request, which adds overhead at scale. Requires CSRF protection for non-GET requests.

---

### 4. Token Authentication
* **What is sent with requests:** A static 40-character hex key inside an authorization header:
  ```http
  Authorization: Token 5c529f8413449c16479065774bc94059b5e64049
  ```
* **Credentials & Expiry:** The user exchanges credentials once at `/login/` for a token. In DRF's default implementation, the token does not expire automatically.
* **Server State:** Stateful. Tokens are persisted in the database (`authtoken_token` table) linked to each user.
* **Verification:** DRF matches the token string against the database to identify the authenticated user.
* **Tradeoffs:**
  * *Pros:* Convenient for mobile apps and CLI clients, does not send passwords with ongoing requests, simple revocation by deleting the token row.
  * *Cons:* Because tokens do not expire by default, compromised tokens remain valid until manually deleted. Each user typically only gets one active token.

---

### 5. JSON Web Token (JWT) Authentication
* **What is sent with requests:** A digitally signed bearer token inside the authorization header:
  ```http
  Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
  ```
* **Credentials & Expiry:** Credentials are exchanged at `/login/` for an access token (15-minute lifetime) and a refresh token (1-day lifetime). When the access token expires, the client calls `/refresh/` with the refresh token to obtain a fresh access token without re-sending the password.
* **Server State:** Stateless. The server does not store active tokens in a database table.
* **Verification:** The server validates the cryptographic signature using its secret key (`SECRET_KEY`) and checks the `exp` timestamp in the payload. If valid, the user identity is trusted directly from the claims.
* **Tradeoffs:**
  * *Pros:* Highly scalable since verification needs no database queries. Granular expiry windows limit the exposure time of leaked access tokens.
  * *Cons:* Cannot easily revoke individual access tokens before expiration without maintaining a blocklist. Token payloads add slightly more bandwidth overhead.

---

## Deep Dive: JWT Architecture

A JSON Web Token consists of three parts separated by periods:
```text
Header.Payload.Signature
```

### Example Decoded JWT

#### 1. Header
Specifies the signing algorithm and token type:
```json
{
  "alg": "HS256",
  "typ": "JWT"
}
```

#### 2. Payload
Contains claims about the user and token lifecycle:
```json
{
  "token_type": "access",
  "exp": 1774224000,
  "iat": 1774223100,
  "jti": "8f3b2a1c9e7d4a5b",
  "user_id": 1
}
```
* `user_id`: Identifies the authenticated user.
* `exp`: Unix timestamp when the token expires.
* `iat`: Unix timestamp when the token was issued.
* `jti`: Unique token identifier used to prevent replay attacks.

#### 3. Signature
Ensures the token cannot be modified:
```text
HMACSHA256(
  base64UrlEncode(Header) + "." + base64UrlEncode(Payload),
  SECRET_KEY
)
```
The server signs the encoded header and payload with its private secret key. If an attacker modifies the payload (for example, altering `user_id`), the signature check fails and the request is rejected with a `401 Unauthorized`.

### Encoding vs Encryption

It is important to note that **JWT payloads are encoded (using Base64URL), not encrypted**.

* **Encoding** transforms data into a standard ASCII format so it can be safely sent over URLs and HTTP headers. Anyone who intercepts a JWT can decode the header and payload using simple tools (or sites like `jwt.io`).
* **Encryption** obfuscates data with a cipher so that only parties with the decryption key can read the plaintext.

Because JWT claims are publicly readable, **sensitive information (passwords, credit card numbers, secret keys) must never be placed inside the payload**. The security of a JWT relies on data integrity and authenticity via the cryptographic signature, not data secrecy.

---

## Validation Rules

1. **Hostel Options:** Only valid campus hostels (Ashok, Bhagirath, Budh, C.V. Raman, Gandhi, Krishna, Malaviya-A/B/C, Malaviya Apts, Rana Pratap, Ram, Shankar, SR, Vishwakarma, Vyas, Meera) are accepted.
2. **Points:** Negative points are rejected by model validators and serializer checks.
3. **Codename:** Cannot be empty or blank whitespace.
4. **State Transitions:**
   * An `unclaimed` mission cannot have a claiming hostel or solver handle.
   * An `in_progress` mission must specify the claiming hostel.
   * A `cracked` mission must specify both the claiming hostel and the `solver_handle`.

---

## Postman Testing

The `postman/` directory contains ready-to-run configurations:
* `Golden_Keyboard.postman_collection.json`
* `Golden_Keyboard.postman_environment.json`

### Steps to Test:
1. Open Postman and click **Import**.
2. Select both JSON files from `postman/`.
3. In the top-right environment dropdown, select **Golden Keyboard - Local**.
4. Run requests individually or run the whole collection via the **Collection Runner**.
   * JWT and Token login requests include test scripts that automatically save `access_token`, `refresh_token`, and `token` into the environment.
   * Test assertions verify both passing requests (`200 OK`, `201 Created`, `204 No Content`) and failing authentication attempts (`401 Unauthorized`, `403 Forbidden`).

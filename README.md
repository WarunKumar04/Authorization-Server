Here’s your complete `README.md` instructions written professionally and clearly for submission:

---

# 🔐 Secure Authentication System

A minimal secure authentication system featuring:

* ✅ **OAuth2-style login** using username and password
* 🔐 **MFA using TOTP (Google Authenticator)**
* 🔑 **JWT Access + Refresh Tokens**
* 🗃️ **MySQL backend for user storage**
* ⚙️ **FastAPI for API endpoints**

---

## 📁 Folder Structure

```
secure_auth_system/
├── app/
│   ├── main.py              # FastAPI app: login, OTP, JWT, protected route
│   ├── database.py          # DB connection + SQLAlchemy model + password utils
│   ├── models.py            # Pydantic schemas
├── create_user.py           # Add new users to the MySQL DB
├── create_tables.py         # Initialize MySQL users table
├── requirements.txt         # Project dependencies
├── generate_qr.py           # (Optional) QR URL generator for TOTP
└── README.md                # Project guide (this file)
```

---

## ⚙️ Step 1: Install Dependencies

Run:

```bash
pip install -r requirements.txt
```

`requirements.txt` should contain:

```txt
fastapi
uvicorn
pyjwt
python-multipart
passlib[bcrypt]
sqlalchemy
pymysql
pyotp
```

---

## 🗃️ Step 2: Configure MySQL

1. Create a MySQL database, e.g. `secure_auth_db`
2. Open `app/database.py`
   Replace the following line with your credentials:

```python
DATABASE_URL = "mysql+pymysql://root:your_password@localhost/secure_auth_db"
```

---

## 🧱 Step 3: Create the `users` Table

Run:

```bash
python create_tables.py
```

This creates the required `users` table in your MySQL database.

---

## 👤 Step 4: Add a New User

To create a user manually:

```bash
python create_user.py
```

This will:

* Hash the password
* Generate a unique TOTP secret
* Save the user to MySQL
* Show the TOTP secret to scan in **Google Authenticator**

---

## 🚀 Step 5: Run the App

Start the FastAPI server:

```bash
uvicorn app.main:app --reload
```

Open your browser at:

👉 [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
Use the interactive Swagger UI to test endpoints.

---

## 🔐 Login & Authentication Flow

### 1. **POST `/login`**

* Accepts:

  * `username`, `password`
* Returns:

  * `{ "otp_required": true, "username": "..." }` if login is successful

---

### 2. **POST `/verify-otp`**

* Accepts:

  * `username`, `otp` (from Google Authenticator)
* Returns:

  * `access_token` (short-lived)
  * `refresh_token` (long-lived)

---

### 3. **GET `/protected`**

* Header:
  `Authorization: Bearer <access_token>`
* Returns:
  Welcome message if token is valid
  Error if token is missing/invalid/expired

---

Let me know if you’d like this exported to a `.md` file, PDF, or need help generating screenshots for documentation.

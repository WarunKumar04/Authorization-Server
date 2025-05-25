from app.database import SessionLocal, User, pwd_context
import pyotp

def create_user(username, password):
    db = SessionLocal()
    hashed = pwd_context.hash(password)
    secret = pyotp.random_base32()

    user = User(username=username, hashed_password=hashed, totp_secret=secret)
    db.add(user)
    db.commit()
    db.close()

    print(f"✅ User created: {username}")
    print(f"🔐 Use this TOTP secret in Google Authenticator: {secret}")

if __name__ == "__main__":
    print("=== User Registration ===")
    username = input("Enter username: ")
    password = input("Enter password: ")
    
    # Call your existing function with the collected inputs
    create_user(username, password)
    
    # Keep the window open
    input("\nPress Enter to exit...")
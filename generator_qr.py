import pyotp

username = "zain"
secret = "6U5TMPR6FLM7YL2OY6NSINZ4N4THQTSG"

print("Secret:", secret)

uri = pyotp.totp.TOTP(secret).provisioning_uri(name=username, issuer_name="SecureAuthApp")
print("Scan this QR code URL in Google Authenticator:")
print("QR Code URL:", uri)



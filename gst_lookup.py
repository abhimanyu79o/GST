import requests
import base64

API_BASE = "http://127.0.0.1:5001"

# Step 1: Get captcha
captcha_resp = requests.get(f"{API_BASE}/api/v1/getCaptcha").json()
session_id = captcha_resp["sessionId"]

# Save captcha image locally
captcha_base64 = captcha_resp["image"].split(",")[1]
with open("captcha.png", "wb") as f:
    f.write(base64.b64decode(captcha_base64))

print("Captcha image saved as captcha.png")
print("Open it, read the captcha, and enter it below.")

# Step 2: Enter GSTIN and captcha
gstin = input("Enter GST Number: ")
captcha_text = input("Enter Captcha Text: ")

# Step 3: Get GST Details
data = {
    "sessionId": session_id,
    "GSTIN": gstin,
    "captcha": captcha_text
}

response = requests.post(f"{API_BASE}/api/v1/getGSTDetails", json=data)
print("\nGST Details Response:")
print(response.json())

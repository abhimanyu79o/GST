import requests
import base64
from PIL import Image
from io import BytesIO

# Step 1: Fetch captcha
captcha_response = requests.get("http://127.0.0.1:5001/api/v1/getCaptcha").json()

# Show captcha image
image_data = captcha_response["image"].split(",")[1]
image = Image.open(BytesIO(base64.b64decode(image_data)))
image.show()

session_id = captcha_response["sessionId"]
gstin = input("Enter GSTIN: ")
captcha = input("Enter Captcha (from image): ")

# Step 2: Fetch GST Details
data = {
    "sessionId": session_id,
    "GSTIN": gstin,
    "captcha": captcha
}

response = requests.post("http://127.0.0.1:5001/api/v1/getGSTDetails", json=data)
print("GST Details:")
print(response.json())

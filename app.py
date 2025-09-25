from flask import Flask, jsonify, request, render_template
import requests
import uuid
import base64

app = Flask(__name__)

gstSessions = {}

@app.route("/", methods=["GET"])
def index():
    # Get captcha
    captcha_url = "https://services.gst.gov.in/services/captcha"
    session = requests.Session()
    session_id = str(uuid.uuid4())

    # Get captcha image
    response = session.get(captcha_url)
    captcha_base64 = base64.b64encode(response.content).decode("utf-8")

    # Save session
    gstSessions[session_id] = {"session": session}

    return render_template("index.html", captcha="data:image/png;base64,"+captcha_base64, session_id=session_id)


@app.route("/getGSTDetails", methods=["POST"])
def getGSTDetails():
    session_id = request.form.get("sessionId")
    gstin = request.form.get("GSTIN")
    captcha = request.form.get("captcha")

    user = gstSessions.get(session_id)
    if not user:
        return "Invalid session ID"

    session = user["session"]

    # Send POST request to GST server
    gst_data = {
        "gstin": gstin,
        "captcha": captcha
    }

    response = session.post("https://services.gst.gov.in/services/api/search/taxpayerDetails", json=gst_data)
    data = response.json()

    return render_template("result.html", gst_data=data)

if __name__ == "__main__":
    app.run(debug=True)

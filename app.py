import os

from dotenv import load_dotenv
from flask import Flask, abort, jsonify, render_template, request
from twilio.request_validator import RequestValidator
from twilio.twiml.messaging_response import MessagingResponse
from werkzeug.middleware.proxy_fix import ProxyFix

load_dotenv()

app = Flask(__name__)
app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)

FAQ = {
    "dengue": (
        "Dengue: use mosquito nets, remove stagnant water, and see a doctor "
        "if fever lasts 2+ days."
    ),
    "hygiene": "Wash hands with soap for 20 seconds.",
}
FALLBACK = "Sorry, I have no verified info on that. Please consult a doctor or call 104."
DISCLAIMER = "Awareness only, not medical advice."


def get_answer(message):
    normalized_message = message.lower()
    return next(
        (value for keyword, value in FAQ.items() if keyword in normalized_message),
        FALLBACK,
    )


@app.get("/")
def home():
    return render_template("index.html")


@app.post("/demo/reply")
def demo_reply():
    data = request.get_json()
    if not isinstance(data, dict) or not isinstance(data.get("message"), str):
        return jsonify(error="Please enter a message."), 400

    answer = get_answer(data["message"])
    return jsonify(reply=f"{answer}\n\n{DISCLAIMER}")


@app.post("/whatsapp")
def whatsapp():
    auth_token = os.getenv("TWILIO_AUTH_TOKEN")
    if not auth_token:
        app.logger.error("TWILIO_AUTH_TOKEN is not configured.")
        abort(500, description="Twilio authentication is not configured.")

    signature = request.headers.get("X-Twilio-Signature", "")
    validator = RequestValidator(auth_token)
    if not validator.validate(request.url, request.form, signature):
        abort(403)

    response = MessagingResponse()
    response.message(get_answer(request.form.get("Body") or "") + "\n\n⚠️ " + DISCLAIMER)
    return str(response), 200, {"Content-Type": "application/xml"}


if __name__ == "__main__":
    app.run(port=5000)

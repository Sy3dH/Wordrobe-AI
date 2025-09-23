import google.auth.transport.requests
from google.oauth2 import service_account
from firebase_admin import messaging, initialize_app, credentials
import os
from dotenv import load_dotenv

load_dotenv()
SCOPES = ["https://www.googleapis.com/auth/firebase.messaging"]

cred = credentials.Certificate(os.getenv("GOOGLE_APPLICATION_CREDENTIALS"))
initialize_app(cred)

def _get_access_token() -> str:
    """
    Retrieve a valid access token that can be used to authorize requests.

    :return: Access token as a string.
    """
    credentials_obj = service_account.Credentials.from_service_account_file(
        cred, scopes=SCOPES
    )
    request = google.auth.transport.requests.Request()
    credentials_obj.refresh(request)
    return credentials_obj.token

def send_notification(token: str, data: dict) -> str:
    """
    Send a message to a device via Firebase Cloud Messaging (FCM).

    :param token: Device registration token from FCM SDK.
    :param data: Dictionary payload to send.
    :return: Message ID string on success.
    """
    message = messaging.Message(data=data, token=token)
    response = messaging.send(message)
    return response

if __name__ == "__main__":
    registration_token = "YOUR_REGISTRATION_TOKEN"
    payload = {"score": "850", "time": "2:45"}

    try:
        msg_id = send_notification(registration_token, payload)
        print("✅ Successfully sent message:", msg_id)
    except Exception as e:
        print("❌ Error sending message:", e)

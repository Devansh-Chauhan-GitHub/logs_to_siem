import base64
import json
import requests
from flask import Flask, request
from google.cloud import storage

WEBHOOK_URL = "https://webhook.site/1d522671-4ddd-41a7-9b52-3801feac0d1e"

app = Flask(__name__)
storage_client = storage.Client()

@app.route("/", methods=["POST"])
def receive_log():
    envelope = request.get_json()

    if not envelope or "message" not in envelope:
        return ("Bad Request", 400)

    try:
        # Decode Pub/Sub message
        pubsub_message = envelope["message"]
        data = base64.b64decode(pubsub_message["data"]).decode("utf-8")
        event = json.loads(data)

        bucket_name = event["bucket"]
        object_name = event["name"]

        # Fetch file content from GCS
        bucket = storage_client.bucket(bucket_name)
        blob = bucket.blob(object_name)

        file_content = blob.download_as_text()

        payload = {
            "event_type": "GCS_OBJECT_CREATE",
            "bucket": bucket_name,
            "object": object_name,
            "metadata": event,
            "file_content": file_content
        }

    except Exception as e:
        print("Processing error:", str(e))
        return ("Processing error", 500)

    # Forward to Webhook.site (SIEM simulation)
    response = requests.post(
        WEBHOOK_URL,
        json=payload,
        timeout=10
    )

    if response.status_code >= 300:
        print("Forwarding failed:", response.text)
        return ("Forward failed", 500)

    return ("OK", 200)


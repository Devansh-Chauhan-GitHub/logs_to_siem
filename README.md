# 🚀 GCP Log File to SIEM Ingestion Pipeline

## 📌 Project Overview

This project demonstrates a **production-grade, event-driven log ingestion pipeline on Google Cloud Platform (GCP)**. Whenever a log file is uploaded to a Google Cloud Storage (GCS) bucket, the system automatically captures the event, reads the actual log file content, and forwards it to an external SIEM endpoint over HTTP.

This project is designed to closely resemble **real-world SIEM ingestion architectures** used in cloud security and DevOps environments.

---

## 🧭 Architecture Diagram

**Live diagram (Eraser):**
[https://app.eraser.io/workspace/a2DBcsPIw1swLUk4Q59S?origin=share](https://app.eraser.io/workspace/a2DBcsPIw1swLUk4Q59S?origin=share)

**Exported PNG:**
![Alt text for the image](/diagram-export-2-2-2026-12_27_24-PM.png)

```text
GCS Bucket → Cloud Audit Logs → Log Sink → Pub/Sub Topic
          → Push Subscription → Cloud Run Service → External SIEM
```

---

## 🧱 Architecture Components

### 1️⃣ Google Cloud Storage (GCS)

* Bucket: `client-log-files-bucket`
* Stores application log files (`.log`, `.txt`)
* Acts as the **event source**

---

### 2️⃣ Cloud Audit Logs

* Automatically generated when objects are created in GCS
* Captures metadata such as:

  * Bucket name
  * Object name
  * Timestamp
  * Object size

> ⚠️ Audit logs **do NOT contain file content** (by design)

---

### 3️⃣ Cloud Logging Sink

* Sink Name: `gcs-to-pubsub-sink`
* Filters only GCS object creation events

```text
resource.type="gcs_bucket"
AND protoPayload.methodName="storage.objects.create"
```

* Routes matching logs to Pub/Sub

---

### 4️⃣ Pub/Sub Topic & Subscription

* Topic: `gcs-new-log-file-topic`
* Subscription: `sap-log-push-sub` (PUSH-based)
* Pushes events to Cloud Run over HTTPS
* Uses **OIDC authentication**

Benefits:

* At-least-once delivery
* Automatic retries
* No polling

---

### 5️⃣ Cloud Run Service (sap-log-forwarder)

Cloud Run acts as the **log processor and forwarder**.

#### Internal Processing Steps:

1. Receives Pub/Sub push message
2. Decodes Base64 payload
3. Extracts bucket name and object name
4. Reads actual log file content from GCS
5. Combines metadata + file content
6. Forwards data to external SIEM endpoint
7. Returns HTTP 200 to ACK Pub/Sub

#### IAM & Security:

* Runs as Compute Engine default service account
* Granted `roles/storage.objectViewer`
* Stateless and auto-scaled

---

### 6️⃣ External SIEM (Webhook.site)

* Used as a **SIEM simulation endpoint**
* Receives structured JSON payload containing:

  * Event metadata
  * Full log file content

---

## 🔐 Security & Reliability Design

* Least-privilege IAM
* Pub/Sub at-least-once delivery
* Automatic retry on failure
* Centralized observability via Cloud Logging

---

## 🧪 End-to-End Flow

```text
1. Upload log file to GCS
2. GCS generates audit log
3. Logging Sink forwards event
4. Pub/Sub stores and pushes message
5. Cloud Run processes event
6. Cloud Run reads file content
7. Payload forwarded to SIEM
8. Pub/Sub message acknowledged
```

---

## 🧪 Testing the Pipeline

### Create a test log file (fish shell)

```bash
printf "ERROR Auth service failed\nWARN Retrying auth\nINFO Service recovered\n" > test-app.log
```

### Upload to GCS

```bash
gsutil cp test-app.log gs://client-log-files-bucket/
```

### Verify Cloud Run execution

```bash
gcloud run services logs read sap-log-forwarder \
  --region asia-south1 \
  --freshness=5m
```

### Verify SIEM ingestion

Check the Webhook.site dashboard to view:

* Metadata
* Actual log file content

---

## 🎯 Why This Architecture?

* Event-driven (no polling)
* Scalable and serverless
* Production-aligned SIEM design
* Secure and observable

---

## 📌 Key Learnings

* Cloud Audit Logs provide **events**, not data
* Pub/Sub enables reliable log transport
* Cloud Run is ideal for stateless log processors
* File content must be explicitly fetched

---

## 📄 Future Enhancements

* File size & type validation
* Dead Letter Queue (DLQ)
* Log parsing (ERROR / WARN / INFO)
* BigQuery archival
* Multi-source log ingestion

---

## 🏁 Conclusion

This project showcases a **real-world, cloud-native log ingestion pipeline** suitable for SIEM integration, security monitoring, and DevOps observability use cases.

It mirrors how modern cloud environments handle log-based events at scale.


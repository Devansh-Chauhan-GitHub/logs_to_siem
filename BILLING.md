# Billing & Cost Estimation – GCP Log to SIEM Architecture

> **Project**: GCP Log to SIEM (Production-grade)
>
> **Scope**: This document explains **all billable components**, links **official GCP pricing documentation**, and provides a **realistic monthly cost estimate** for the complete setup.
>
> ⚠️ All costs are **approximate**, calculated using **public GCP pricing** and **reasonable assumptions**. Actual bills may vary based on region, traffic, and usage patterns.

---

## 1. Architecture Components Covered

This billing covers the following services used in the project:

1. Cloud Logging
2. Logging Sinks
3. Pub/Sub
4. Cloud Run (service)
5. Cloud Storage (GCS)
6. Artifact Registry
7. Cloud Build / GitHub Actions (if applicable)
8. Networking (egress)
9. IAM (no cost, but mentioned for completeness)

---

## 2. Cloud Logging

### What is billed

* Log ingestion
* Log storage (beyond free tier)
* Log routing via sinks

### Free Tier

* **50 GB/month** log ingestion is free

### Assumptions

* 20 GB logs/month ingested
* Logs retained for 30 days

### Cost

* Ingestion: **FREE (within 50 GB)**
* Storage: Included in ingestion pricing

### Estimated Monthly Cost

**$0.00**

### Reference

* [https://cloud.google.com/logging/pricing](https://cloud.google.com/logging/pricing)

---

## 3. Log Router / Logging Sink

### What is billed

* Log routing to Pub/Sub

### Cost

* **Log routing is FREE**

### Estimated Monthly Cost

**$0.00**

### Reference

* [https://cloud.google.com/logging/docs/routing/overview](https://cloud.google.com/logging/docs/routing/overview)

---

## 4. Pub/Sub

### What is billed

* Message publishing
* Message delivery (push)

### Free Tier

* 10 GB/month message volume free

### Assumptions

* 20 GB/month log data

### Pricing

* First 10 GB: Free
* Remaining 10 GB @ ~$40/TB

### Cost Calculation

* 10 GB × $0.04/GB ≈ **$0.40**

### Estimated Monthly Cost

**~$0.40**

### Reference

* [https://cloud.google.com/pubsub/pricing](https://cloud.google.com/pubsub/pricing)

---

## 5. Cloud Run (Log Processor Service)

### What is billed

* CPU time
* Memory usage
* Request count

### Free Tier

* 2 million requests/month
* 360,000 vCPU-seconds
* 180,000 GiB-seconds

### Assumptions

* Requests: 300,000/month
* CPU: 0.5 vCPU
* Memory: 512 MB
* Execution time: 1 second/request

### Usage Calculation

* vCPU-seconds: 150,000 (within free tier)
* GiB-seconds: ~150,000 (within free tier)

### Estimated Monthly Cost

**$0.00**

### Reference

* [https://cloud.google.com/run/pricing](https://cloud.google.com/run/pricing)

---

## 6. Cloud Storage (GCS)

### What is billed

* Object storage
* Operations (GET/LIST)
* Data retrieval

### Assumptions

* 10 GB stored logs/files
* Standard storage class

### Pricing

* ~$0.020 per GB/month

### Cost Calculation

* 10 GB × $0.02 = **$0.20**

### Estimated Monthly Cost

**~$0.20**

### Reference

* [https://cloud.google.com/storage/pricing](https://cloud.google.com/storage/pricing)

---

## 7. Artifact Registry

### What is billed

* Image storage

### Free Tier

* First 0.5 GB free

### Assumptions

* Docker images: 1 GB

### Cost Calculation

* 0.5 GB × $0.10 ≈ **$0.05**

### Estimated Monthly Cost

**~$0.05**

### Reference

* [https://cloud.google.com/artifact-registry/pricing](https://cloud.google.com/artifact-registry/pricing)

---

## 8. Cloud Build / CI

### What is billed

* Build minutes

### Free Tier

* 120 build-minutes/day

### Assumptions

* Using GitHub Actions OR minimal Cloud Build

### Estimated Monthly Cost

**$0.00**

### Reference

* [https://cloud.google.com/build/pricing](https://cloud.google.com/build/pricing)

---

## 9. Network Egress (SIEM Integration)

### What is billed

* Outbound internet traffic

### Assumptions

* Logs sent to external SIEM
* 20 GB/month egress

### Pricing (approx)

* ~$0.12/GB

### Cost Calculation

* 20 GB × $0.12 = **$2.40**

### Estimated Monthly Cost

**~$2.40**

### Reference

* [https://cloud.google.com/vpc/network-pricing](https://cloud.google.com/vpc/network-pricing)

---

## 10. IAM

### Cost

* **IAM has no direct cost**

### Reference

* [https://cloud.google.com/iam/pricing](https://cloud.google.com/iam/pricing)

---

## 11. Total Monthly Cost Summary

| Service           | Estimated Cost     |
| ----------------- | ------------------ |
| Cloud Logging     | $0.00              |
| Pub/Sub           | $0.40              |
| Cloud Run         | $0.00              |
| Cloud Storage     | $0.20              |
| Artifact Registry | $0.05              |
| Network Egress    | $2.40              |
| **Total**         | **~$3.05 / month** |

---


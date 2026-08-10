
# Spotify End-to-End Data Engineering Pipeline (AWS)

An automated, event-driven ETL pipeline that extracts music data from the Spotify API, transforms it, and loads it into a queryable data store — built entirely on AWS serverless services.

---

## Overview

This project demonstrates a real-world, production-style data engineering pipeline. It continuously pulls data from the Spotify API, processes it through a series of automated stages, and makes it available for SQL-based analysis — with no manual intervention required at any step.

**Key characteristics:**
- Fully automated and event-driven (each stage triggers the next)
- Serverless architecture (no servers to manage or maintain)
- Near real-time data extraction (runs every 1 minute)
- Query-ready output via SQL (Amazon Athena)

---

## Architecture

🚀 SIEM with ELK Stack (Elasticsearch, Logstash, Kibana, Filebeat & ElastAlert2)
📌 Overview

This project implements a Security Information and Event Management (SIEM) system using the ELK stack with alerting via ElastAlert2.

It simulates SSH authentication logs using a custom Python log generator, ingests those logs with Filebeat, parses and enriches them in Logstash, stores and indexes them in Elasticsearch, visualizes them in Kibana, and generates alerts with ElastAlert2 when suspicious activity is detected.

✅ Beginner-friendly — demonstrates end-to-end SIEM pipeline.
✅ Real-time log ingestion, search, visualization, and alerting.
✅ Modular and extendable to other log sources.

🏗 Architecture
[ Python Log Generator ]
          ↓
[ Filebeat ] → ships logs
          ↓
[ Logstash ] → parses with grok, enriches fields
          ↓
[ Elasticsearch ] → indexes & stores logs
          ↓
[ Kibana ] → dashboards, queries, visualizations
          ↓
[ ElastAlert2 ] → runs rules on ES indices & triggers alerts

🔧 Components
1. Log Generator

Python script to simulate auth.log style SSH events (success/fail).

Produces logs with fields like timestamp, username, source IP, status.

Useful for testing ingestion without needing real servers.

2. Filebeat

Lightweight log shipper.

Monitors generated log files.

Sends logs to Logstash for parsing.

3. Logstash

Central data pipeline.

Parses raw logs using grok filters.

Extracts fields: @timestamp, user, src_ip, status, action.

Sends structured JSON events to Elasticsearch.

4. Elasticsearch

Distributed search and analytics engine.

Stores parsed events in indices (filebeat-*).

Provides fast search and aggregations.

5. Kibana

Web UI for Elasticsearch.

Features:

Explore logs in Discover.

Build visualizations and dashboards.

Manage index patterns and data views.

SOC-style dashboards (failed logins, top source IPs, user activity).

6. ElastAlert2

Rule-based alerting engine for Elasticsearch.

Runs queries on indices periodically.

Triggers alerts when conditions match (e.g., brute-force attempts).

Writes alerts into elastalert_status index (can be viewed in Kibana).

⚡ Features

✅ Ingests custom logs in real-time.

✅ Uses grok to parse unstructured log messages.

✅ Stores normalized logs in Elasticsearch.

✅ Provides dashboards in Kibana.

✅ Alerts on suspicious activity (e.g., multiple failed SSH logins).

📂 Project Structure
SIEM-ELK-Project/
│
├── docker-compose.yml        # Docker setup for ELK + ElastAlert
├── log_generator.py          # Python script simulating SSH logs
│
├── filebeat/
│   └── filebeat.yml          # Filebeat configuration
│
├── logstash/
│   └── pipeline/
│       └── logstash.conf     # Logstash pipeline (grok parsing)
│
├── elastalert/
│   ├── config.yaml           # ElastAlert global config
│   └── rules/
│       └── ssh_bruteforce.yaml  # Example alert rule
│
└── README.md                 # Documentation

⚙️ Setup & Installation
1. Clone repository
git clone https://github.com/your-username/SIEM-ELK-Project.git
cd SIEM-ELK-Project

2. Start ELK stack
docker-compose up -d


Check running containers:

docker ps


You should see es, kibana, logstash, filebeat, elastalert.

3. Generate logs

Run the Python log generator:

python3 log_generator.py


Logs will be written to a file (e.g., auth.log) that Filebeat is monitoring.

4. Verify Elasticsearch
docker exec -it es curl -X GET "http://localhost:9200/_cat/indices?v"

5. Access Kibana

Open browser: http://localhost:5601

Create data view (e.g., filebeat-*).

Explore logs in Discover.

Build dashboards.

6. Alerts (ElastAlert2)

Example rule: detect more than 5 failed SSH logins from same IP in 1 minute.

Alerts written into elastalert_status index.

Can be visualized in Kibana.

🔔 Example Alert Rule (ssh_bruteforce.yaml)
name: "SSH Brute Force Detection"
type: frequency
index: filebeat-*
num_events: 5
timeframe:
  minutes: 1
filter:
- term:
    status: "failed"
alert:
- "elasticsearch"
alert_text: "Multiple failed SSH logins detected from {0}"
alert_text_args: ["src_ip"]
alert_text_type: alert_text_only

📊 Example Dashboard Ideas

Failed logins over time (line chart).

Top source IPs causing failed logins.

Top targeted usernames.

Alerts table from elastalert_status index.

🚨 Use Cases

🔐 Detect brute-force SSH attacks.

🛡 Track user login activity.

📈 Monitor suspicious IP addresses.

📂 Extendable for other logs (web server, firewall, Windows events).

📖 Interview Talking Points

Explain log flow step by step (Log Generator → Filebeat → Logstash → Elasticsearch → Kibana → ElastAlert).

Emphasize why grok (parsing raw logs).

Describe ElastAlert rules (frequency-based, real-time detection).

Show Kibana dashboards (SOC use cases).

Mention scalability (Kafka, ILM policies, multi-node ES).

✅ Next Improvements

Add Metricbeat for system monitoring.

Use Kafka as buffer for scalability.

Enable TLS + Authentication for security.

Add Index Lifecycle Management (ILM) to control storage costs.

🏁 Conclusion

This project demonstrates a miniature SIEM using open-source tools.
It covers log generation, ingestion, parsing, storage, visualization, and alerting — the full pipeline of a SOC workflow.

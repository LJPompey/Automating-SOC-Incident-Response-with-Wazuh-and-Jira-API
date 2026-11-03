#!/usr/bin/env python3
import sys, json, requests
from requests.auth import HTTPBasicAuth

# 1. Jira Cloud Credentials & Config
JIRA_DOMAIN = "https://lamontpompeyjr-projectx.atlassian.net"
JIRA_USER = "YOUR_EMAIL@DOMAIN.COM" # Your Atlassian login email
JIRA_API_TOKEN = "YOUR_API_TOKEN"
PROJECT_KEY = "IT" # Matches your IT Service Project

# 2. Read the Wazuh Alert JSON (Wazuh passes the file path as argument 1)
try:
    with open(sys.argv[1], 'r') as alert_file:
        alert = json.load(alert_file)
except Exception as e:
    sys.exit(1)

# 3. Extract Log Data
rule_desc = alert.get("rule", {}).get("description", "Unknown Wazuh Alert")
full_log = alert.get("full_log", "No raw log provided.")
agent_name = alert.get("agent", {}).get("name", "Unknown Agent")

# 4. Format the Jira API Payload (API v3)
api_url = f"{JIRA_DOMAIN}/rest/api/3/issue"
payload = {
    "fields": {
        "project": {"key": PROJECT_KEY},
        "issuetype": {"name": "[System] Incident"}, 
        "summary": f"[SIEM ALERT] {rule_desc} on {agent_name}",
        "description": {
            "type": "doc",
            "version": 1,
            "content": [
                {
                    "type": "paragraph",
                    "content": [{"type": "text", "text": f"Agent Name: {agent_name}\n\nRaw Log: {full_log}"}]
                }
            ]
        }
    }
}

# 5. Execute POST Request
response = requests.post(
    api_url,
    json=payload,
    auth=HTTPBasicAuth(JIRA_USER, JIRA_API_TOKEN)
)

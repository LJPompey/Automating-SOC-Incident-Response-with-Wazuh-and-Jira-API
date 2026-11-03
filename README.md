# Automated SOC Pipeline & Detection Engineering

## 📌 Overview
This project demonstrates a high-fidelity, locally hosted Security Operations Center (SOC) automation pipeline. By integrating a Wazuh SIEM with Jira Service Management via a custom Python webhook, this architecture automatically detects malicious endpoint activity and orchestrates immediate incident ticket creation, complete with 15-minute Critical SLA tracking aligned with ITIL principles.

## 🏗️ Architecture & Infrastructure
This environment is hosted locally within a 7-node VMware Workstation enterprise lab (`Project X`). 

**Technology Stack:**
*   **SIEM:** Wazuh (Locally Hosted)
*   **ITSM / Ticketing:** Jira Service Management (Cloud)
*   **Middleware:** Python 3 (API Webhooks, `requests` library)
*   **Endpoints:** Ubuntu Linux (Target), Kali Linux (Attacker)
*   **Network:** Local `10.0.0.0/24` virtualized network

## ⚙️ The Workflow
1.  **Attack Simulation:** A brute-force SSH attack is launched from a Kali Linux VM against a target Ubuntu endpoint using Hydra and the SecLists `fasttrack.txt` wordlist.
2.  **Telemetry & Detection:** The Wazuh agent installed on the Ubuntu endpoint forwards the rapid authentication failures to the Wazuh Manager. The manager correlates the events and triggers a Level 10 `SSHD Brute Force` alert.
3.  **Automation Trigger:** The Wazuh `integratord` daemon detects the Level 10 threshold breach and executes a custom Python script (`custom-jira`), passing the raw JSON alert data as an argument.
4.  **Ticket Orchestration:** The Python script parses the JSON for the agent name, rule description, and raw log output, authenticates with the Atlassian Cloud API, and POSTs a formatted payload.
5.  **SLA Enforcement:** A high-priority Incident ticket is instantly generated in Jira with a 15-minute Time-to-First-Response SLA, delivering the raw log context directly to the SOC analyst.

## 📸 Proof of Concept
*(Add your screenshots here)*
1.  `![Kali Hyrda Attack](Hydra-Attack.png)` - **Attack Execution**
2.  `[Screenshot 2: Wazuh dashboard showing the Level 10 alert]` - **SIEM Detection**
3.  `[Screenshot 3: Nano editor showing the Python webhook script]` - **API Orchestration**
4.  `[Screenshot 4: Jira Service Management ticket with SLA timer]` - **ITSM Ticket Generation**

## 💻 The Integration Script
The custom Python webhook developed for this pipeline utilizes Atlassian Document Format (ADF) to properly structure the raw log data into the Jira ticket description block. 
*(Link to your custom-jira.py file in the repository)*

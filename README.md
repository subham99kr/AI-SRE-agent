# 🤖 AI-SRE: Multi-Agent Kubernetes Incident Response System

> An AI-powered Site Reliability Engineering (SRE) platform that investigates Kubernetes incidents, determines root causes, generates explainable remediation plans, and safely automates recovery using a multi-agent architecture.

![Python](https://img.shields.io/badge/Python-3.11+-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-Backend-green)
![LangGraph](https://img.shields.io/badge/LangGraph-Multi--Agent-orange)
![Kubernetes](https://img.shields.io/badge/Kubernetes-Production-blue)
![Docker](https://img.shields.io/badge/Docker-Containerized-2496ED)
![License](https://img.shields.io/badge/License-MIT-yellow)

---

## 📖 Overview

Modern Kubernetes environments generate thousands of alerts every day, leaving engineers to manually inspect logs, events, deployments, and cluster resources before identifying the actual root cause.

AI-SRE automates this investigation process using a team of specialized AI agents. Instead of simply answering questions, it follows an SRE-style workflow:

* Collect relevant Kubernetes evidence
* Identify the incident type
* Investigate the probable root cause
* Generate an explainable remediation plan
* Assess execution risk
* Safely execute approved actions
* Verify cluster recovery

The platform is built using **LangGraph**, **FastAPI**, and the **Kubernetes Python Client**, enabling structured reasoning and safe automation for production Kubernetes environments.

---

## ✨ Key Features

* 🔍 Automated Kubernetes incident investigation
* 🤖 Multi-agent workflow powered by LangGraph
* 📊 Evidence-driven root cause analysis
* 📚 Incident-specific investigation playbooks
* ⚠️ Risk-aware remediation planning
* 👨‍💻 Human-in-the-loop approval support
* 🚀 Automated Kubernetes recovery actions
* ✅ Post-remediation health verification
* 📜 Persistent investigation and execution history
* 🔌 Modular architecture for adding new incident types

---
## 🏗️ High-Level Architecture

```mermaid
flowchart LR

A[Monitoring / Alert]
--> B[Collect Evidence]

B --> C[Classify Incident]

C --> D[Collect Adaptive Evidence]

D --> E[Format Evidence]

E --> F[Root Cause Analysis]

F --> G{Enough Evidence?}

G -->|No| H[Collect More Evidence]

H --> E

G -->|Yes| I[Plan Remediation]

G -->|Max Attempts| J[Fallback]

I --> K{Approval Required?}

K -->|Yes| L[Human Approval]

K -->|No| M[Execute Remediation]

L --> M

M --> N[Verify Recovery]

N --> O[Generate Summary]

O --> P[Persist Incident]
J --> P
```
---

## 🤖 AI Agent Pipeline

Each agent is responsible for a single stage of the incident lifecycle.

| Agent               | Responsibility                          |
| ------------------- | --------------------------------------- |
| Evidence Builder    | Collect Kubernetes resources and events |
| Incident Classifier | Determine the failure category          |
| Playbook Engine     | Select the investigation strategy       |
| Reasoning Agent     | Identify the most likely root cause     |
| Planning Agent      | Generate remediation steps              |
| Risk Assessment     | Evaluate operational risk               |
| Approval Agent      | Request human approval when needed      |
| Execution Agent     | Apply approved Kubernetes actions       |
| Verification Agent  | Confirm successful recovery             |

This modular design keeps the workflow explainable, maintainable, and easy to extend with new incident types.

---

## 🎯 Supported Incident Types

AI-SRE currently supports investigation workflows for common Kubernetes failures, including:

* CrashLoopBackOff
* OOMKilled
* Pending Pods
* ImagePullBackOff
* Failed Liveness Probes
* Failed Readiness Probes
* DNS Resolution Issues
* Persistent Volume Failures
* Node Resource Exhaustion

Additional playbooks can be added without modifying the overall workflow.

---

## 🔄 Investigation Workflow

Every incident follows a structured investigation pipeline before any action is taken.

```mermaid
flowchart LR

Alert
--> CollectEvidence

CollectEvidence
--> ClassifyIncident

ClassifyIncident
--> CollectAdaptiveEvidence

CollectAdaptiveEvidence
--> FormatEvidence

FormatEvidence
--> RootCauseAnalysis

RootCauseAnalysis
--> Decision{Enough Evidence?}

Decision
-->|No| CollectMoreEvidence

CollectMoreEvidence
--> FormatEvidence

Decision
-->|Yes| RemediationPlan

Decision
-->|Max Attempts| ManualInvestigation

RemediationPlan
--> RiskAssessment
```

### Investigation Stages

| Stage                   | Description                                                      |
| ----------------------- | ---------------------------------------------------------------- |
| Evidence Collection     | Gather relevant Kubernetes resources, events, logs, and metadata |
| Incident Classification | Detect the type of Kubernetes failure                            |
| Playbook Selection      | Choose an investigation strategy based on the incident           |
| Root Cause Analysis     | Analyze evidence using AI reasoning                              |
| Remediation Planning    | Generate a safe recovery plan                                    |
| Risk Assessment         | Determine whether approval is required                           |

The investigation phase is **read-only** and never modifies the Kubernetes cluster.

---

## ⚡ Execution Workflow

After an investigation is completed, AI-SRE executes the approved remediation plan.

```mermaid
flowchart LR

LoadIncident
--> CheckApproval

CheckApproval
--> ExecuteRemediation

ExecuteRemediation
--> VerifyRecovery

VerifyRecovery
--> GenerateSummary

GenerateSummary
--> PersistResults

PersistResults
--> Complete
```

### Execution Pipeline

1. Validate the remediation plan.
2. Execute Kubernetes operations.
3. Verify workload health.
4. Generate an execution report.
5. Store execution history for auditing.

Depending on the configured risk policy, execution can be fully automated or require human approval.

---

## 📁 Project Structure

```text
ai-sre/
├── app/
│   ├── api/                # FastAPI endpoints
│   ├── agents/             # AI agents
│   ├── graph/              # LangGraph workflow
│   ├── playbooks/          # Incident playbooks
│   ├── tools/              # Kubernetes tools
│   ├── services/           # Business logic
│   ├── models/             # Pydantic models
│   ├── database/           # PostgreSQL integration
│   └── config/
│
├── frontend/               # React UI
├── deployments/            # Docker & Kubernetes manifests
├── tests/
├── docs/
└── README.md
```

---

## 🛠️ Technology Stack

| Category         | Technologies                          |
| ---------------- | ------------------------------------- |
| Backend          | FastAPI, Python                       |
| AI Orchestration | LangGraph, LangChain                  |
| LLM Providers    | OpenAI, Gemini, Groq *(configurable)* |
| Kubernetes       | Kubernetes Python Client              |
| Database         | PostgreSQL                            |
| Containerization | Docker                                |
| Frontend         | React                                 |
| Observability    | LangSmith                             |

---

## 🔍 Why AI-SRE?

Unlike traditional monitoring tools that stop after generating alerts, AI-SRE continues the incident lifecycle by:

* Investigating the root cause
* Correlating Kubernetes evidence
* Recommending explainable remediation steps
* Executing approved actions safely
* Verifying that the issue has actually been resolved

The result is a faster, more consistent incident response process with reduced manual effort.

---
## 🚀 Getting Started

### Prerequisites

Before running AI-SRE, ensure you have:

* Python 3.11+
* Docker
* Kubernetes cluster (Kind, Minikube, or a cloud cluster)
* PostgreSQL
* An LLM API key (OpenAI, Gemini, or Groq)

---

### Installation

```bash
# Clone the repository
git clone https://github.com/subham99kr/ai-sre-agent.git

cd ai-sre

# Create a virtual environment
python -m venv .venv

# Activate the environment
# Linux / macOS
source .venv/bin/activate

# Windows
.venv\scripts\activate

# Install dependencies
pip install -r requirements.txt
```

---

### Configure Environment

Create a `.env` file in the project root.

```env
LLM_PROVIDER=gemini

GOOGLE_API_KEY=your_api_key

DATABASE_URL=postgresql://user:password@localhost:5432/aisre

KUBECONFIG=/path/to/kubeconfig
```

---

### Run the Application

Start the backend server:

```bash
uvicorn app.main:app --reload
```

The API will be available at:

```
http://localhost:8000
```

Swagger documentation:

```
http://localhost:8000/docs
```

---

## 💡 Example Workflow

1. An alert is received for a Kubernetes workload.
2. AI-SRE gathers relevant cluster information.
3. The incident is classified.
4. A root cause analysis is performed.
5. A remediation plan is generated.
6. If required, the plan is approved by an operator.
7. AI-SRE executes the approved action.
8. The system verifies that the workload has recovered.

---

## 🛣️ Roadmap

### Current

* ✅ Multi-agent investigation workflow
* ✅ Kubernetes evidence collection
* ✅ Root cause analysis
* ✅ Remediation planning
* ✅ Risk-aware execution
* ✅ Verification workflow

### Planned

* 🔄 Prometheus metrics integration
* 🔄 Grafana dashboard analysis
* 🔄 Slack / Microsoft Teams notifications
* 🔄 Multi-cluster support
* 🔄 Historical incident search
* 🔄 RAG-powered operational knowledge base

---

## 🤝 Contributing

Contributions are welcome!

If you'd like to improve AI-SRE:

1. Fork the repository.
2. Create a feature branch.
3. Commit your changes.
4. Open a Pull Request.

For major changes, please open an issue first to discuss the proposed design.

---

## 📄 License

This project is licensed under the **MIT License**.

See the `LICENSE` file for details.

---

## ⭐ Support

If you found this project useful:

* ⭐ Star the repository
* 🐛 Report bugs by opening an issue
* 💡 Suggest new features or playbooks
* 🤝 Contribute improvements

Your feedback and contributions help make AI-SRE better for the community.

---

<p align="center">
Built with ❤️ using <strong>FastAPI</strong>, <strong>LangGraph</strong>, <strong>Kubernetes</strong>, and <strong>Python</strong>.
</p>


# AI-SRE: Autonomous Kubernetes Incident Investigation & Self-Healing Platform

> An AI-powered Site Reliability Engineering (SRE) platform that autonomously investigates Kubernetes incidents, identifies their root causes, recommends or executes remediations, verifies recovery, and maintains a complete investigation history.

---

# Motivation

Modern cloud-native applications run on Kubernetes clusters that may contain hundreds or even thousands of containers. While Kubernetes provides self-healing capabilities such as restarting failed containers and rescheduling pods, it does **not** diagnose *why* failures occur or determine the most appropriate corrective action.

In production environments, incidents such as:

* CrashLoopBackOff
* ImagePullBackOff
* Failed Scheduling
* OOMKilled Containers
* Probe Failures
* Configuration Errors
* Resource Exhaustion
* Persistent Volume Issues

can lead to service degradation or complete outages.

When these incidents occur, Site Reliability Engineers (SREs) typically perform a repetitive investigation process:

1. Inspect Kubernetes events.
2. Collect pod logs.
3. Examine deployment specifications.
4. Analyze resource utilization.
5. Review previous deployment history.
6. Correlate evidence from multiple sources.
7. Determine the root cause.
8. Decide on an appropriate remediation.
9. Execute the remediation.
10. Verify that the deployment has recovered.

Although these steps are well understood, they remain largely manual, time-consuming, and dependent on individual expertise.

For organizations operating multiple Kubernetes clusters, even a single production incident can consume significant engineering effort while delaying service restoration.

---

# The Problem

Manual incident investigation introduces several operational challenges:

* Increased Mean Time To Detect (MTTD)
* Increased Mean Time To Resolve (MTTR)
* Repetitive investigation across similar incidents
* Delayed recovery during production outages
* Human error during diagnosis and remediation
* Inconsistent incident handling across engineering teams
* Loss of valuable troubleshooting knowledge after incidents are resolved

Longer outages not only affect application availability but also lead to wasted compute resources, reduced engineering productivity, missed service-level objectives (SLOs), and potential financial losses.

---

# Our Solution

AI-SRE automates the complete Kubernetes incident response lifecycle.

Instead of relying solely on predefined rules or alerts, AI-SRE combines:

* Kubernetes API inspection
* Prometheus metrics
* Adaptive evidence collection
* Incident-specific playbooks
* Large Language Models (LLMs)
* Automated remediation planning
* Deployment verification
* Historical incident memory

to provide an end-to-end autonomous investigation pipeline.

The platform separates **decision making** from **execution**, ensuring that high-risk operations can still require human approval while low-risk remediations can be performed automatically.

Rather than replacing SREs, AI-SRE acts as an intelligent operational assistant capable of dramatically reducing investigation time and accelerating recovery.

---

# Objectives

AI-SRE is designed to:

* Reduce Mean Time To Detect (MTTD)
* Reduce Mean Time To Resolve (MTTR)
* Minimize manual Kubernetes debugging
* Standardize incident investigation
* Provide explainable root cause analysis
* Recommend safe remediations
* Support automated execution where appropriate
* Preserve investigation history for future incidents
* Improve operational reliability across multiple Kubernetes clusters

---

# Key Features

## Multi-Cluster Management

* Register multiple Kubernetes clusters
* Independent kubeconfig management
* Cluster-specific investigations
* Cluster-specific Prometheus integration

---

## Automated Evidence Collection

Automatically gathers operational evidence including:

* Deployments
* ReplicaSets
* Pods
* Events
* Logs
* Resource configuration
* Node information
* Kubernetes metadata

---

## Adaptive Investigation

Rather than collecting every available resource, AI-SRE dynamically selects additional evidence based on the detected incident type using predefined playbooks.

This significantly reduces unnecessary data collection while improving diagnostic accuracy.

---

## AI-Powered Root Cause Analysis

Large Language Models analyze the collected evidence together with incident-specific playbooks and previous investigation history to determine:

* Root Cause
* Confidence Score
* Supporting Evidence

---

## Intelligent Remediation Planning

Generates remediation plans that include:

* Recommended actions
* Kubectl commands
* Risk assessment
* Rollback availability
* Human approval requirements
* Operational reasoning

---

## Automated Execution

Approved remediation steps can be executed automatically.

Every executed command records:

* Command
* Execution status
* Standard output
* Error output

forming a complete execution audit trail.

---

## Recovery Verification

Following remediation, AI-SRE continuously validates deployment health by checking rollout progress, pod readiness, deployment availability, and recovery status before declaring the incident resolved.

---

## Persistent Incident Memory

Every investigation is stored for future reference.

When similar incidents occur again, AI-SRE incorporates previous investigation summaries into the reasoning process, enabling iterative learning and preventing repeated unsuccessful remediation attempts.

---

## Monitoring Installer

The project includes a lightweight monitoring installer that:

* Deploys Prometheus
* Configures RBAC
* Creates persistent storage
* Registers Kubernetes clusters
* Exports kubeconfig files
* Supports Windows and Linux

without requiring Helm or cloud-provider-specific tooling.

---

# High-Level Architecture

```text
                    +----------------------+
                    |   Kubernetes Cluster |
                    +----------+-----------+
                               |
             +-----------------+-----------------+
             |                                   |
             ▼                                   ▼
      Kubernetes API                     Prometheus Metrics
             |                                   |
             +-----------------+-----------------+
                               |
                               ▼
                 Evidence Collection Layer
                               |
                               ▼
                  Incident Classification
                               |
                               ▼
                Adaptive Evidence Collection
                               |
                               ▼
                  Root Cause Analysis (LLM)
                               |
                               ▼
                 Intelligent Remediation Plan
                               |
                               ▼
                    Human Approval (Optional)
                               |
                               ▼
                   Automated Command Execution
                               |
                               ▼
                    Deployment Verification
                               |
                               ▼
                    Incident Report Generation
                               |
                               ▼
                     Persistent Incident Memory
```

---

# Technology Stack

| Category           | Technologies            |
| ------------------ | ----------------------- |
| Language           | Python                  |
| Workflow Engine    | LangGraph               |
| LLM Framework      | LangChain               |
| Kubernetes         | Kubernetes API, Kubectl |
| Monitoring         | Prometheus              |
| Backend            | FastAPI                 |
| Database           | SQLite / SQLAlchemy     |
| AI Models          | OpenAI Compatible LLMs  |
| Container Platform | Docker, Kubernetes      |
| Version Control    | Git                     |
| Operating Systems  | Windows, Linux          |



# System Architecture

AI-SRE is designed as a modular platform where every component has a single responsibility. This separation makes the system extensible, easier to test, and allows individual modules to evolve independently.

At a high level, the platform consists of six major layers.

```text
                    ┌──────────────────────────┐
                    │       React Frontend     │
                    └─────────────┬────────────┘
                                  │
                                  ▼
                    ┌──────────────────────────┐
                    │      FastAPI Backend     │
                    └─────────────┬────────────┘
                                  │
                ┌─────────────────┴─────────────────┐
                │                                   │
                ▼                                   ▼
      Investigation Workflow             Execution Workflow
          (LangGraph)                       (LangGraph)
                │                                   │
                └───────────────┬───────────────────┘
                                ▼
                     Kubernetes Service Layer
                                │
               ┌────────────────┴─────────────────┐
               │                                  │
               ▼                                  ▼
        Kubernetes API                     Prometheus API
               │                                  │
               └────────────────┬─────────────────┘
                                ▼
                         Target Cluster
```

The frontend provides operators with visibility into cluster health, incidents, investigations, remediation plans, and execution history.

The FastAPI backend exposes REST APIs, manages workflows, persists investigation history, and coordinates communication between AI agents and Kubernetes.

The LangGraph workflows orchestrate the complete investigation and remediation lifecycle while maintaining state across every stage of execution.

---

# Investigation Workflow

The investigation workflow is responsible for understanding **what happened**, **why it happened**, and **what should be done**. It focuses entirely on reasoning and decision making without modifying the Kubernetes cluster.

## Investigation Graph

```text
                               START
                                 │
                                 ▼
                  Load Previous Investigation
                                 │
                                 ▼
                    Collect Initial Evidence
                                 │
                                 ▼
                     Classify Incident Type
                                 │
                                 ▼
                  Collect Adaptive Evidence
                                 │
                                 ▼
                       Format Evidence
                                 │
                                 ▼
                    Root Cause Analysis (LLM)
                                 │
                                 ▼
                     Generate Remediation Plan
                                 │
                                 ▼
                      Approval Decision
                                 │
                                 ▼
                    Persist Investigation
                                 │
                                 ▼
                                END
```

---

## 1. Load Previous Investigation

Before beginning a new investigation, AI-SRE determines whether the current incident is a retry of a previous failed remediation.

If previous attempts exist, summaries of earlier investigations are loaded into the workflow.

This enables the reasoning agent to avoid repeatedly recommending unsuccessful remediation strategies.

---

## 2. Collect Initial Evidence

The Evidence Builder gathers the minimum information required to understand the deployment's current state.

Examples include:

* Deployment specification
* ReplicaSets
* Pod status
* Pod events
* Container logs
* Namespace information
* Kubernetes metadata

At this stage the objective is to build a concise snapshot of the deployment without collecting unnecessary information.

---

## 3. Incident Classification

The Incident Classifier analyzes the collected evidence and categorizes the failure into a known incident type.

Typical categories include:

* CrashLoopBackOff
* ImagePullBackOff
* Pending Pods
* OOMKilled
* Probe Failures
* Scheduling Failures
* Configuration Errors

Incident classification determines which investigation playbook will be executed during the next stage.

---

## 4. Adaptive Evidence Collection

Rather than collecting every Kubernetes resource, AI-SRE uses playbooks to gather only the information relevant to the detected incident.

Examples include:

CrashLoopBackOff

* Previous ReplicaSets
* Restart history
* Probe configuration

OOMKilled

* Resource limits
* Resource requests
* Container memory metrics

ImagePullBackOff

* Image name
* Pull secrets
* Registry configuration

Scheduling Failure

* Node capacity
* Taints
* Affinity rules

This adaptive approach significantly reduces investigation time while improving reasoning quality.

---

## 5. Evidence Formatting

Raw Kubernetes objects are difficult for language models to reason over directly.

The formatter converts the collected evidence into a structured representation that:

* removes unnecessary metadata
* preserves operational context
* minimizes prompt size
* improves LLM reasoning efficiency

---

## 6. Root Cause Analysis

The Root Cause Agent receives:

* formatted evidence
* incident type
* playbook knowledge
* previous investigation summaries

Using this information, the LLM determines:

* probable root cause
* confidence score
* supporting reasoning

Unlike rule-based systems, the reasoning process incorporates multiple evidence sources simultaneously.

---

## 7. Remediation Planning

Once the root cause has been identified, the Remediation Agent proposes a recovery strategy.

The generated plan contains:

* remediation steps
* kubectl commands
* operational reasoning
* estimated risk
* rollback availability
* approval requirement

Each remediation step is represented as executable Kubernetes operations that can later be reviewed or executed automatically.

---

## 8. Approval

Every remediation passes through an approval stage.

Three possible outcomes exist:

### No Action Required

The deployment is healthy or no corrective action is necessary.

---

### Automatically Approved

Low-risk operations may be executed without operator intervention.

Examples:

* rollout restart
* scale deployment
* delete failed pod

---

### Pending Human Approval

Potentially disruptive operations require manual approval.

Examples include:

* deleting resources
* modifying deployment configuration
* updating container images
* changing ConfigMaps
* modifying Secrets

This separation allows safe automation without sacrificing operational control.

---

## 9. Persist Investigation

Finally, the complete investigation is stored within the database.

Persisted information includes:

* Incident
* Evidence
* Root Cause
* Confidence
* Remediation Plan
* Approval Status

The generated Incident ID becomes the starting point of the execution workflow.

---

# Why Separate Investigation from Execution?

A common limitation of many autonomous remediation systems is that reasoning and execution are tightly coupled.

AI-SRE intentionally separates these responsibilities.

The Investigation Workflow focuses exclusively on answering:

* What failed?
* Why did it fail?
* What is the safest remediation?

Only after an investigation has been reviewed or approved does the Execution Workflow begin.

This separation provides:

* safer automation
* human oversight for risky operations
* reproducible investigations
* complete audit trails
* the ability to retry execution without repeating the investigation

# Execution Workflow

Unlike the Investigation Workflow, which focuses on reasoning and decision making, the **Execution Workflow** is responsible for safely applying approved remediations, validating cluster recovery, and maintaining a complete execution history.

The workflow is intentionally separated from investigation so that execution can occur immediately after approval or at a later time without repeating the diagnostic process.

---

# Execution Graph

```text
                           START
                             │
                             ▼
                    Load Investigation
                             │
                             ▼
                  Execute Remediation
                             │
                             ▼
                Verify Deployment Health
                  (Automatic Retries)
                             │
                             ▼
                 Generate Execution Report
                             │
                             ▼
                  Persist Execution Result
                             │
                             ▼
                            END
```

---

# 1. Load Investigation

The workflow begins by loading the previously completed investigation using the Incident ID.

Rather than recomputing the root cause, the workflow retrieves all previously generated information, including:

* Cluster information
* Namespace
* Deployment
* Incident type
* Root cause
* Collected evidence
* Remediation plan
* Risk assessment

This separation allows investigations to be performed once while execution can occur multiple times if necessary.

---

# 2. Execute Remediation

The Execution Agent is responsible for applying the approved remediation plan to the target Kubernetes cluster.

Each remediation step contains:

* Human-readable description
* Kubectl command
* Expected outcome

For every step, AI-SRE records:

* Executed command
* Success or failure
* Standard output
* Standard error
* Execution timestamp

Example:

```text
Step 1
Rollout Restart Deployment

kubectl rollout restart deployment sample-backend

Status
✓ Success
```

If any command fails, execution stops immediately.

This prevents partially applied remediations from causing additional instability.

---

# Command Execution Layer

Instead of executing shell commands directly throughout the codebase, every Kubernetes operation is routed through a dedicated Kubectl Tool.

The tool automatically:

* Loads the correct kubeconfig
* Selects the correct cluster
* Executes commands
* Captures output
* Reports execution status

This abstraction keeps all Kubernetes communication centralized and makes supporting multiple clusters significantly simpler.

---

# Multi-Cluster Execution

Every incident stores its originating Cluster ID.

Before executing any remediation, AI-SRE automatically loads the corresponding kubeconfig and switches to the correct cluster.

This guarantees that remediation commands are always executed against the intended environment.

```text
Incident

↓

Cluster ID

↓

Load kubeconfig

↓

Execute kubectl command

↓

Target Cluster
```

This design enables the platform to safely manage multiple Kubernetes clusters simultaneously.

---

# 3. Verification

Successfully executing commands does not necessarily mean that the deployment has recovered.

For example:

* Rollout restart may fail.
* New pods may still crash.
* Readiness probes may continue failing.
* Replica count may remain unavailable.

Therefore, every remediation is followed by an independent verification stage.

---

# Verification Strategy

The Verification Agent repeatedly evaluates deployment health.

Typical checks include:

* Deployment exists
* Desired replicas available
* Updated replicas available
* Pods Ready
* Rollout completed
* No CrashLoopBackOff
* No Pending replicas

Rather than checking only once, verification retries several times with configurable delays.

```text
Verification Attempt 1

↓

Deployment unhealthy

↓

Wait

↓

Verification Attempt 2

↓

Deployment unhealthy

↓

Wait

↓

Verification Attempt 3

↓

Deployment healthy

↓

Success
```

This retry strategy avoids false failures caused by Kubernetes still performing a rollout.

---

# 4. Execution Report Generation

Once verification completes, the Summarizer Agent produces a structured operational report.

The report includes:

## Incident Summary

* Cluster
* Namespace
* Deployment
* Incident type

---

## Root Cause

The diagnosis produced during the investigation.

---

## Remediation Summary

* Commands executed
* Execution status
* Failures
* Risk level

---

## Verification Results

* Deployment health
* Recovery status
* Verification outcome

---

## Operational Summary

A concise explanation describing:

* what happened
* what actions were taken
* whether recovery was successful
* remaining concerns

This report provides engineers with a complete narrative of the incident.

---

# 5. Persistence

The final workflow stage stores the execution results.

Persisted information includes:

## Execution History

* Commands executed
* Success status
* Output
* Errors

---

## Verification

* Verification attempts
* Deployment health
* Final status

---

## Report

* Generated summary
* Operational recommendations
* Recovery confirmation

Maintaining this execution history enables future investigations to learn from previous remediation attempts.

---

# Why Persist Execution?

Historical execution data provides several advantages:

* Complete audit trail
* Regulatory compliance
* Incident timeline reconstruction
* Retry optimization
* Operational analytics
* Continuous improvement

Future investigations can incorporate previous execution outcomes to avoid repeating unsuccessful remediation strategies.

---

# Complete AI-SRE Lifecycle

```text
                    Kubernetes Incident
                             │
                             ▼
                  Investigation Workflow
                             │
                             ▼
                 Root Cause Identified
                             │
                             ▼
                Remediation Plan Created
                             │
                             ▼
                    Approval Decision
                             │
               ┌─────────────┴─────────────┐
               │                           │
               ▼                           ▼
        Pending Approval            Auto Approved
               │                           │
               └─────────────┬─────────────┘
                             ▼
                  Execution Workflow
                             │
                             ▼
                 Execute Kubernetes Commands
                             │
                             ▼
                Verify Deployment Recovery
                             │
                             ▼
                  Generate Execution Report
                             │
                             ▼
                  Persist Investigation Data
                             │
                             ▼
                     Incident Resolved
```

---

# Design Philosophy

The platform intentionally separates **reasoning**, **execution**, and **verification** into independent stages.

This architecture provides several important advantages:

* Investigations remain reproducible.
* Executions can be retried without repeating expensive AI reasoning.
* Human approval can be inserted before any high-risk action.
* Every remediation is independently verified.
* Complete investigation and execution histories are preserved for future learning.

By combining deterministic Kubernetes operations with LLM-assisted reasoning, AI-SRE delivers an autonomous yet auditable incident response system suitable for modern multi-cluster Kubernetes environments.


## Investigation Workflow

Validated against incidents including:

* CrashLoopBackOff
* ImagePullBackOff
* Pending Pods
* OOMKilled
* Failed Readiness Probe
* Failed Liveness Probe
* Resource Exhaustion
* Invalid Image
* Scheduling Failure
* Replica Failure

---

# Current Limitations

AI-SRE is an actively evolving project.

Current limitations include:

* Supports Kubernetes workloads only.
* Relies on Prometheus for metrics collection.
* Root cause quality depends on the completeness of collected evidence.
* Investigation quality depends on available playbooks.
* Some high-risk remediations intentionally require manual approval.

---

# Future Enhancements

Planned improvements include:

* Grafana integration
* Alertmanager integration
* Prometheus Operator support
* Distributed investigation across clusters
* Automatic incident prioritization
* Continuous cluster health monitoring
* Fine-tuned LLMs for Kubernetes troubleshooting
* Retrieval-Augmented Generation (RAG) over Kubernetes documentation
* Historical trend analysis
* Cost-aware remediation recommendations
* Support for additional cloud providers
* Policy-driven autonomous remediation
* Multi-agent collaboration for complex failures

---

# Why LangGraph?

Traditional automation systems execute fixed sequences of predefined steps.

AI-SRE uses LangGraph because incident investigation is inherently stateful and adaptive.

LangGraph enables:

* Persistent workflow state
* Conditional execution paths
* Retry logic
* Human-in-the-loop approvals
* Separation of reasoning and execution
* Clear orchestration of AI agents

This makes the investigation pipeline easier to extend, debug, and maintain as new incident types and capabilities are added.

---

# Acknowledgements

This project builds upon several outstanding open-source technologies:

* Kubernetes
* Prometheus
* LangChain
* LangGraph
* FastAPI
* SQLAlchemy
* Docker

Their ecosystems provide the foundation that enables AI-SRE to automate modern cloud-native operations.

---


# Final Note

AI-SRE demonstrates how Large Language Models can be integrated with Kubernetes observability, deterministic automation, and structured workflows to build an intelligent operational assistant for modern cloud-native systems.

Rather than replacing Site Reliability Engineers, the platform augments their capabilities by reducing repetitive investigation effort, accelerating root cause analysis, standardizing remediation workflows, and preserving operational knowledge for future incidents.


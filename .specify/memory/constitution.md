<!--
Sync Impact Report:
- Version change: None -> 1.0.0
- Added sections:
  - Core Principles
  - Security
  - Governance
- Templates requiring updates:
  - ✅ /Users/ojiman/Devel/istock-monitor/.specify/templates/plan-template.md
-->

# istock-monitor Constitution

## Core Principles

### Reliability (信頼性)
The primary goal is to provide accurate stock information. The system must be robust against potential errors (e.g., network issues, changes in Apple's API response) and operate stably.

### Efficiency (効率性)
The process runs frequently, so it must be lightweight and consume minimal resources. Slack notifications should only be sent when there is a change in stock status to avoid unnecessary alerts.

### Clarity (明瞭性)
The Slack notification output must be clear and instantly understandable. It should explicitly state what is in stock, where, and when.

### Maintainability (保守性)
Product models and target store information may change. The system should be designed so that these variables can be easily updated without altering the core logic.

### Simplicity (シンプルさ)
The project's scope is focused on stock checking and notification. It should avoid unnecessary complexity and stick to its core function.

## Security
Secrets, such as the Slack Webhook URL, must be managed using GitHub Secrets and must never be hardcoded into the source code.

## Governance
This is a personal project managed by the repository owner. The owner makes all key decisions.

**Version**: 1.0.0 | **Ratified**: 2025-09-21 | **Last Amended**: 2025-09-21

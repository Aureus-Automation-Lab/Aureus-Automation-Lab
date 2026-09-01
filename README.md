# Aureus Automation Lab

[![Ecosystem](https://img.shields.io/badge/Aureus-Enterprise%20Automation%20Suite-blueviolet?style=for-the-badge&logo=shield)](https://github.com/Aureus-Automation-Lab)
[![Architecture](https://img.shields.io/badge/Architecture-Tier--1%20Autonomous%20Systems-00C853?style=for-the-badge)](https://github.com/AureusAutomationLab)
[![Compliance](https://img.shields.io/badge/Standards-FAANG%20%2F%20Zero--Leakage-blue?style=for-the-badge)](docs/products/public-boundary.md)

**Controlled AI automation, financial workflow operating systems, and high-throughput enterprise infrastructure.**

Founded & Engineered by **Róbert Kolesár** and **Patrik Trnavský**

![Aureus controlled AI automation hero](assets/aureus-profile-hero.gif)

---

## The Master Ecosystem Architecture

Aureus Automation Lab is not a disconnected collection of scripts; it is a **coherent, 4-tier enterprise automation and operating platform**:

```mermaid
flowchart TD
    subgraph Tier1["Tier 1: Financial OS & Document Automation (FinEcon)"]
        FE_P[FinEcon Pocket<br/>Flutter / iOS & Android] --> FE_Core[FinEcon Core Orchestrator<br/>20 n8n Workflows & AI Engine]
        FE_W[FinEcon Web & Portal<br/>React 18 / TypeScript] --> FE_Core
        FE_Core --> ERP[POHODA ERP Bridge<br/>mServer XML Integration]
        FE_Core --> EPOST[ePoštár Gateway<br/>e-Faktúra 2026/2027 Peppol BIS 3.0]
    end

    subgraph Tier2["Tier 2: Operational Health & Telemetry (OpsPulse)"]
        OP_API[OpsPulse Telemetry Engine<br/>FastAPI / Python 3.12]
        OP_M[OpsPulse Mobile Dashboard<br/>React Native / Expo]
        FE_Core -.->|Heartbeat & Metrics| OP_API
        OP_API --> OP_M
    end

    subgraph Tier3["Tier 3: Quantitative & High-Throughput (Aureus Trading)"]
        TR_INFRA[Aureus Tick Infra<br/>Event-Driven L0/L1/L2 Pipeline]
        TR_EXEC[Risk-Gated Binance Futures Executor<br/>Redis State & Prometheus Observability]
        TR_INFRA --> TR_EXEC
        TR_EXEC -.->|Health & Telemetry| OP_API
    end

    subgraph Tier4["Tier 4: Multimodal Edge & Speech (Captions TV)"]
        CAP_TV[Aureus Captions TV<br/>Streaming WebSocket ASR & Neural MT]
    end
```

---

## Products & Platform Suites

| Suite / System | Repository | Primary Purpose | Tech Stack & Output |
| :--- | :--- | :--- | :--- |
| **FinEcon Ecosystem** | [AureusAutomationLab/FinEcon](https://github.com/AureusAutomationLab/FinEcon)<br>[AureusAutomationLab/n8n-workflows](https://github.com/AureusAutomationLab/n8n-workflows) | End-to-end finance operating system: field receipt capture, AI parsing, pre-accounting, POHODA XML bridge, and e-Faktúra 2026/2027 ePoštár gateway. | • **Pocket App:** Flutter (iOS/Android)<br>• **Web:** React 18 / TypeScript / Vite<br>• **Core:** n8n (20 Workflows) / Azure OpenAI<br>• **Gateways:** POHODA mServer & Peppol BIS 3.0 |
| **OpsPulse** | [AureusAutomationLab/opspulse](https://github.com/AureusAutomationLab/opspulse) | Centralized microservice health monitoring, operational telemetry, and anomaly alerting. | • **Backend:** FastAPI / Python 3.12<br>• **Mobile:** React Native / Expo<br>• **Alerts:** Telegram Dispatcher & Webhooks |
| **Aureus Trading Infra** | [AureusAutomationLab/aureus-trading](https://github.com/AureusAutomationLab/aureus-trading) | Event-driven quantitative tick infrastructure, order book analytics, and risk-gated execution. | • **Engine:** Python 3.11 / Redis<br>• **Observability:** Prometheus & Grafana<br>• **Security:** Hardware-isolated exchange executor |
| **Aureus Captions TV** | [Aureus-Automation-Lab/aureus-captions-tv](https://github.com/Aureus-Automation-Lab/aureus-captions-tv) | Low-latency streaming audio ingestion, real-time speech recognition (ASR), and multilingual subtitle broadcast for Android TV. | • **Server:** Python / WebSockets / Docker<br>• **Target:** Android TV Leanback & Connected Displays |

---

## Microservice Blueprints & Templates

Standardized starter templates for repeatable, compliant service delivery:

* **[aal-worker-template](https://github.com/AureusAutomationLab/aal-worker-template):** Python 3.12 background worker with CLI, JSON logging, and health checks.
* **[aal-web-saas-template](https://github.com/AureusAutomationLab/aal-web-saas-template):** Next.js, TypeScript, and Tailwind CSS web SaaS starter with local auth.
* **[aal-python-service-template](https://github.com/AureusAutomationLab/aal-python-service-template):** FastAPI microservice blueprint with Pydantic contracts and automated pytest suite.

---

## Operating Governance & Delivery Standard

Aureus operates on the **Silicon Valley Tier-1 Autonomous Protocol**:

1. **Human-in-the-Loop Governance:** High-risk actions (accounting ledgers, payments, regulatory filings) require explicit review and authorization gates.
2. **Deterministic State Management:** Zero loose or undocumented scripts; all business pipelines run on versioned, test-verified workflows.
3. **Defense in Depth & Zero Secrets:** Zero credentials or real customer financial records in source repositories; all secrets are managed via hardware/OS-level secret stores.
4. **Verifiable Proof Packs:** Cryptographic SHA-256 signatures generated for every batch of processed financial documents.

---

## Public Documentation & Deep Dives

* 📖 **[FinEcon Product Guide](docs/products/finecon.md)** – Detailed three-pillar architecture and workflow breakdown.
* 🏛️ **[Public Proof Showroom](public-proof/README.md)** – Public-safe architectural evidence, data contracts, and review models.
* 🛡️ **[Public Security Boundary](docs/products/public-boundary.md)** – Strict boundaries protecting proprietary IP and client privacy.
* 💼 **[Engagement & Offer Menu](docs/products/offers.md)** – Pilot programs, automation audits, and monthly partnership retainers.

---

## Public Web Surfaces

* **Main Portal:** [https://aureus.it.com/automationlab](https://aureus.it.com/automationlab)
* **FinEcon Hub:** [https://aureus.it.com/finecon](https://aureus.it.com/finecon)

---

## Summary

Aureus Automation Lab provides unified, production-grade AI automation and finance operating systems connecting mobile capture, intelligent workflows, ERPs, telemetry, and electronic invoicing.

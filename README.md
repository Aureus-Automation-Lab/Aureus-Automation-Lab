<div align="center">

# 🏛️ AUREUS AUTOMATION LAB
### **Enterprise AI Automation, Financial Operating Systems & High-Throughput Infrastructure**

```
   █████╗ ██╗   ██╗██████╗ ███████╗██╗   ██╗███████╗   ██╗      █████╗ ██████╗ 
  ██╔══██╗██║   ██║██╔══██╗██╔════╝██║   ██║██╔════╝   ██║     ██╔══██╗██╔══██╗
  ███████║██║   ██║██████╔╝█████╗  ██║   ██║███████╗   ██║     ███████║██████╔╝
  ██╔══██║██║   ██║██╔══██╗██╔══╝  ██║   ██║╚════██║   ██║     ██╔══██║██╔══██╗
  ██║  ██║╚██████╔╝██║  ██║███████╗╚██████╔╝███████║██╗███████╗██║  ██║██████╔╝
  ╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═╝╚══════╝ ╚═════╝ ╚══════╝╚═╝╚══════╝╚═╝  ╚═╝╚═════╝ 
```

<p align="center">
  <a href="https://github.com/Aureus-Automation-Lab"><img src="https://img.shields.io/badge/Aureus-Enterprise%20Suite-7C3AED?style=for-the-badge&logo=shield&logoColor=white" alt="Aureus Suite" /></a>
  <a href="https://github.com/AureusAutomationLab"><img src="https://img.shields.io/badge/Architecture-Tier--1%20Autonomous%20Systems-00C853?style=for-the-badge&logo=codeforces&logoColor=white" alt="Tier-1 Autonomous" /></a>
  <a href="docs/products/public-boundary.md"><img src="https://img.shields.io/badge/Security-Zero--Leakage%20Guarantee-0070F3?style=for-the-badge&logo=lock&logoColor=white" alt="Zero-Leakage" /></a>
  <a href="https://aureus.it.com/automationlab"><img src="https://img.shields.io/badge/Web-aureus.it.com-FF0080?style=for-the-badge&logo=vercel&logoColor=white" alt="Web Portal" /></a>
</p>

<p align="center">
  <strong>Controlled AI automation for companies that require speed, mathematical accuracy, and human-in-the-loop governance.</strong>
</p>

<p align="center">
  Founded & Engineered by <strong>Róbert Kolesár</strong> and <strong>Patrik Trnavský</strong>
</p>

---

[ 📊 Architecture ](#-master-ecosystem-architecture) • 
[ 💼 FinEcon Ecosystem ](#-1-finecon-ecosystem--financial-operating-system) • 
[ 🦅 Identity Intel ](#-2-aureus-identity-intel--autonomous-osint--biometrics) • 
[ 📡 OpsPulse ](#-3-opspulse--telemetry--observability) • 
[ 📈 Trading Infra ](#-4-aureus-trading-infra--quantitative-engine) • 
[ 🛡️ Proof Showroom ](#-public-proof-showroom--tamper-evident-evidence) • 
[ 🚀 Commercial Pilots ](#-commercial-pilots--engagement)

---

![Aureus controlled AI automation hero](assets/aureus-profile-hero.gif)

</div>

---

## 🗺️ Master Ecosystem Architecture

Aureus Automation Lab operates on a **5-tier unified architecture** designed to bridge physical field operations, machine intelligence, high-consequence enterprise ERPs, and low-latency infrastructure:

```mermaid
flowchart TD
    subgraph Tier1["1. Financial Operating System (FinEcon)"]
        FE_P["📱 FinEcon Pocket<br/>Flutter / iOS & Android"] --> FE_Core["⚙️ FinEcon Core Orchestrator<br/>20 n8n Pipelines & AI Vision"]
        FE_W["💻 FinEcon Web Portal<br/>React 18 / TypeScript / Vite"] --> FE_Core
        FE_Core --> ERP["🏢 POHODA ERP Bridge<br/>mServer XML (PriFaktury, Pokladna, IntDoklady)"]
        FE_Core --> EPOST["🇪🇺 ePoštár Gateway<br/>e-Faktúra 2026/2027 Peppol BIS 3.0 / UBL 2.1"]
    end

    subgraph Tier2["2. Autonomous Intelligence & OSINT (Identity Intel)"]
        INT_SENS["🌐 Multi-Vector OSINT Network<br/>Web, Registries & Digital Footprints"] --> INT_ENG["🦅 Identity Intel Engine<br/>FastAPI / Python 3.12"]
        INT_ENG --> INT_BIO["👤 512-D Biometric Face Matcher<br/>Cosine Similarity Filter >= 0.68"]
        INT_ENG --> INT_RESOLV["🧠 Fellegi-Sunter Entity Resolution<br/>Probabilistic Graph Matching"]
    end

    subgraph Tier3["3. Operational Health & Telemetry (OpsPulse)"]
        OP_API["📡 OpsPulse Ingestion Core<br/>FastAPI / Python 3.12"]
        OP_M["📱 OpsPulse Mobile Dispatcher<br/>React Native / Expo"]
        FE_Core -.->|Heartbeat & Metrics| OP_API
        INT_ENG -.->|Telemetry| OP_API
        OP_API --> OP_M
    end

    subgraph Tier4["4. Quantitative Tick Infrastructure (Aureus Trading)"]
        TR_INFRA["⚡ Aureus Tick Infra<br/>Event-Driven L0/L1/L2 Pipeline"]
        TR_EXEC["🔒 Risk-Gated Binance Futures Executor<br/>Redis State & Prometheus Observability"]
        TR_INFRA --> TR_EXEC
        TR_EXEC -.->|Health & Telemetry| OP_API
    end

    subgraph Tier5["5. Multimodal Edge & Speech (Captions TV)"]
        CAP_TV["📺 Aureus Captions TV<br/>Streaming WebSocket ASR & Neural MT"]
    end
```

---

## 💎 Product Showcase & Platform Suites

<div align="center">

### 💼 1. FinEcon Ecosystem – Financial Operating System
*The premier Slovak & European financial automation suite connecting mobile intake to ERP accounting ledgers.*

</div>

<table>
  <tr>
    <td width="55%">
      <h4>🌟 Key Highlights:</h4>
      <ul>
        <li><strong>FinEcon Pocket (Mobile):</strong> Cross-platform Flutter app for iOS & Android with offline-first capture, local draft restore, and 1-tap in-app approval.</li>
        <li><strong>AI Pre-Accounting Engine:</strong> Automatic Slovak accounting classification (<code>518</code>, <code>501</code>, <code>602</code>, <code>604</code>, <code>511</code>), EU reverse-charge samozdanenie (<code>aInt</code>/<code>bInt</code>), and vehicle fuel statutory splits (CAR 50:50 / 80:20).</li>
        <li><strong>POHODA ERP mServer Bridge:</strong> Schema-validated XML generation for <code>PriFaktury</code>, <code>VydFaktury</code>, <code>Pokladna</code>, and <code>IntDoklady</code> with gated dry-run preflight checks.</li>
        <li><strong>e-Faktúra 2026/2027 & ePoštár Gateway:</strong> Turnkey Peppol BIS 3.0 / UBL 2.1 e-invoicing adapter with HMAC-SHA256 signed push webhook ingress.</li>
      </ul>
      <p>
        <a href="docs/products/finecon.md"><img src="https://img.shields.io/badge/Read-Product%20Deep%20Dive-7C3AED?style=flat-square" alt="Deep Dive"/></a>
        <a href="https://github.com/AureusAutomationLab/FinEcon"><img src="https://img.shields.io/badge/Repo-FinEcon%20Web-blue?style=flat-square" alt="Web Repo"/></a>
        <a href="https://github.com/AureusAutomationLab/n8n-workflows"><img src="https://img.shields.io/badge/Repo-n8n%20Workflows%20%26%20Pocket-00C853?style=flat-square" alt="Workflows Repo"/></a>
      </p>
    </td>
    <td width="45%">
      <img src="assets/aureus-finecon-flow.gif" alt="FinEcon Review Flow" width="100%"/>
    </td>
  </tr>
</table>

---

<div align="center">

### 🦅 2. Aureus Identity Intel – Autonomous OSINT & Biometrics
*Tier-1 entity resolution, facial biometrics, and multi-vector intelligence platform.*

</div>

<table>
  <tr>
    <td width="45%">
      <img src="assets/evidence-ledger-flow.svg" alt="Identity Intel Flow" width="100%"/>
    </td>
    <td width="55%">
      <h4>⚡ Capabilities:</h4>
      <ul>
        <li><strong>Multi-Vector Triangulation:</strong> Correlates names, aliases, emails, phone numbers, registries, and digital footprints.</li>
        <li><strong>512-D Biometric Matcher:</strong> High-precision vector face embeddings with cosine similarity filtering ($\ge 0.68$) to confirm identity across unlinked platforms.</li>
        <li><strong>Fellegi-Sunter Probabilistic Resolution:</strong> Mathematical entity resolution separating homonyms and resolving multi-source profiles.</li>
        <li><strong>NetworkX Knowledge Graph:</strong> In-memory topological graph with native exports for Neo4j, Memgraph, and STIX2.</li>
      </ul>
      <p>
        <a href="https://github.com/AureusAutomationLab/aureus-identity-intel"><img src="https://img.shields.io/badge/Repo-aureus--identity--intel-3776AB?style=flat-square&logo=python&logoColor=white" alt="Identity Intel Repo"/></a>
      </p>
    </td>
  </tr>
</table>

---

<div align="center">

### 📡 3. OpsPulse – Telemetry & Observability
*Real-time microservice health aggregation, latency telemetry, and anomaly alerting.*

</div>

<table>
  <tr>
    <td width="55%">
      <h4>📊 Core Features:</h4>
      <ul>
        <li><strong>Centralized Ingestion Core:</strong> High-throughput FastAPI (Python 3.12) telemetry service collecting heartbeat signals across all distributed nodes.</li>
        <li><strong>Mobile Monitoring Dashboard:</strong> React Native / Expo client giving executives and operations leads real-time system pulse on iOS & Android.</li>
        <li><strong>Automated Telegram Incident Dispatcher:</strong> Instant multi-channel alert delivery when error thresholds or latency limits are breached.</li>
      </ul>
      <p>
        <a href="https://github.com/AureusAutomationLab/opspulse"><img src="https://img.shields.io/badge/Repo-OpsPulse-blueviolet?style=flat-square" alt="OpsPulse Repo"/></a>
      </p>
    </td>
    <td width="45%">
      <img src="assets/github-command-center-flow.svg" alt="Command Center Flow" width="100%"/>
    </td>
  </tr>
</table>

---

<div align="center">

### 📈 4. Aureus Trading Infra – Quantitative Engine
*Event-driven tick processing, order book telemetry, and risk-gated futures execution.*

</div>

* **Deterministic 3-Stage Pipeline:** L0 (Tick Normalization) $\rightarrow$ L1 (Signal Synthesis) $\rightarrow$ L2 (Risk Gate & Execution).
* **Isolated Exchange Key Boundary:** Only the hardened execution daemon holds API keys; zero raw credentials exposed to strategy layers.
* **Observability Stack:** Redis runtime state store paired with native Prometheus exporters and Grafana operational dashboards.

<p align="center">
  <a href="https://github.com/AureusAutomationLab/aureus-trading"><img src="https://img.shields.io/badge/Repo-aureus--trading-black?style=flat-square&logo=binance&logoColor=yellow" alt="Trading Repo"/></a>
</p>

---

## 🏛️ Public Proof Showroom – Tamper-Evident Evidence

Aureus systems operate under strict **non-repudiation and cryptographic auditability**. Every processed document batch produces a verifiable **Proof Pack** with SHA-256 state hashes:

<div align="center">

| Proof Category | Architectural Diagram | Description & Verification |
| :--- | :---: | :--- |
| **FinEcon Flow & POHODA Gateway** | <img src="assets/finecon-invoice-boundary.svg" width="320"/> | Gated transition from raw mobile capture to verified POHODA mServer XML. |
| **Audit Ledger & Proof Hash** | <img src="assets/evidence-ledger-flow.svg" width="320"/> | Tamper-evident event ledger storing SHA-256 byte signatures for legal compliance. |
| **Aureus Operating Boundary** | <img src="assets/public-private-boundary.svg" width="320"/> | Strict boundary ensuring zero private credentials or customer data in public space. |

[👉 Explore the Complete Public Proof Showroom](public-proof/README.md)

</div>

---

## 🛡️ The 4 Golden Principles of Aureus

```text
1. AI Prepares    ──► Models extract, itemize, normalize, and draft candidate records.
2. Humans Approve ──► Certified operators and managers retain 100% review authority.
3. Systems Prove  ──► Every mutation generates an immutable, cryptographic audit pack.
4. Zero Risk      ──► Gated execution, dry-run preflights, and zero unhandled fallbacks.
```

---

## 💼 Commercial Pilots & Engagement

We partner with **accounting bureaus, field-intensive enterprises, and growing SMEs** to implement end-to-end automation with guaranteed ROI:

* 🏢 **FinEcon Pilot Program:** Turnkey deployment of FinEcon Pocket for your field staff + POHODA mServer automated pre-accounting bridge.
* 🔍 **Automation Audit (Process Discovery):** Detailed mapping of manual bottlenecks, ROI modeling, and a phased automation blueprint.
* 🤝 **Monthly Automation Partner Retainer:** Continuous pipeline engineering, 24/7 OpsPulse monitoring, and dedicated infrastructure support.

---

<div align="center">

### 🚀 Ready to Automate Your Business Operations?

[![Website](https://img.shields.io/badge/Website-aureus.it.com%2Fautomationlab-FF0080?style=for-the-badge&logo=googlechrome&logoColor=white)](https://aureus.it.com/automationlab)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-Connect%20with%20Founders-0A66C2?style=for-the-badge&logo=linkedin&logoColor=white)](https://linkedin.com)
[![Email](https://img.shields.io/badge/Contact-Direct%20Inquiry-00C853?style=for-the-badge&logo=gmail&logoColor=white)](mailto:kimi.aoki.if@gmail.com)

<br/>

<sub>© 2026 Aureus Automation Lab. Engineered for Autonomous Reliability & Enterprise Excellence.</sub>

</div>

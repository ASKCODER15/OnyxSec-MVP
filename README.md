[U<div align="center">
  
# 🛡️ ONYXSEC.AI
**The Immune System for AI-Generated Infrastructure.**

*Built for the IBM Call for Code Global Challenge: Assist & Amplify Track*

</div>

---

## ⚠️ The Threat to Frontline Organizations
Non-Governmental Organizations (NGOs) and human rights activists are increasingly relying on generative AI tools (such as Lovable, v0, and ChatGPT) to rapidly build digital applications for victim outreach and resource mapping. 

**The Problem:** AI excels at generating Frontend User Interfaces but notoriously generates highly insecure backend code.
If trafficking syndicates exploit these AI-generated vulnerabilities (such as Broken Access Control or exposed API keys), they can access NGO databases, unmasking whistleblower identities and exposing safehouse locations. In this field, insecure code costs lives.

## 💡 Our Solution: OnyxSec
OnyxSec is an automated, AI-driven Code Auditing and Security Dossier platform designed specifically to intercept vulnerable AI-generated code before it reaches production.

### Core Features:
*   **The AI Security Tribunal:** OnyxSec doesn't rely on a single model. Users can toggle a **Multi-Model Consensus Engine** that simultaneously queries multiple state-of-the-art LLMs (like Meta's Llama 3.3 70B) to cross-examine code and ensure zero vulnerabilities are missed.
*   **Deterministic Threat Scoring:** To prevent LLM hallucinations, OnyxSec utilizes a hardcoded Python mathematical engine that calculates a strict Risk Score (0-100) based on the severity of the OWASP Top 10 vulnerabilities detected.
*   **Interactive Security Dossier:** Instead of auto-fixing the code (which creates lazy developers), OnyxSec acts as a strict Senior Engineer. It flags the vulnerabilities, forces the developer to rewrite the code, and mathematically verifies their fix.

---

## 🛠️ Technology Stack & Architecture
This MVP was engineered to demonstrate the feasibility of automated security injection, with a roadmap to scale onto enterprise infrastructure.

*   **Frontend / UI:** Python & Streamlit (Featuring a custom Neo-Brutalist 3D design system).
*   **AI Inference Engine:** Groq API (Utilizing Llama 3.3 70B for deep architectural audits).
*   **Enterprise Roadmap:** The production version of OnyxSec is designed to integrate natively with **IBM Cloud Object Storage** and **IBM Watsonx.ai** to guarantee absolute data sovereignty for our NGO partners.

---

## 🚀 How to Run the OnyxSec MVP Locally

If you wish to test the Security Dossier simulator locally, follow these steps:

1. **Clone the repository:**
   ```bash
   https://github.com/ASKCODER15/OnyxSec-MVP.git
   ```
2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
3. **Run the application:**
   ```bash
   streamlit run app.py
   ```
4. **Configuration:**
   * Obtain a free API key from [Groq Console](https://console.groq.com/).
   * Paste the key into the OnyxSec configuration sidebar to initiate a scan.

---
<div align="center">
  <i>"We can democratize application development for underfunded NGOs, while guaranteeing mathematically secure privacy for the survivors they protect."</i>
</div>ploading README.md…]()


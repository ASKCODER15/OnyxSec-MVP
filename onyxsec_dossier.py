import streamlit as st
from groq import Groq
import re

# ═════════════════════════════════════════════════════════════════════════════
# PAGE CONFIG
# ═════════════════════════════════════════════════════════════════════════════
st.set_page_config(
    page_title="OnyxSec — Code Audit Dossier",
    page_icon="◆",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ═════════════════════════════════════════════════════════════════════════════
# DESIGN TOKENS — "Security Dossier" direction
# Deep graphite + warm parchment text + hazard-amber for flags + muted teal
# for verified/secure. Stamp motif = signature element. No neon hacker cliché.
# ═════════════════════════════════════════════════════════════════════════════
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@500;700&family=IBM+Plex+Sans:wght@400;500;600&family=JetBrains+Mono:wght@400;500;700&display=swap');

:root {
    --bg: #15171C;
    --surface: #1C1F26;
    --surface-deep: #11131A;
    --border: #2C2F38;
    --text: #EDEAE3;
    --text-dim: #9CA0AC;
    --amber: #E2572B;
    --amber-soft: rgba(226,87,43,0.12);
    --orange: #E08A3C;
    --orange-soft: rgba(224,138,60,0.12);
    --yellow: #D9B14A;
    --yellow-soft: rgba(217,177,74,0.12);
    --teal: #45A98A;
    --teal-soft: rgba(69,169,138,0.12);
    --blue: #5B8DBE;
}

html, body, [class*="css"] { font-family: 'IBM Plex Sans', sans-serif; color: var(--text); }
.stApp { background: var(--bg); }

/* ── Case file header ── */
.case-header {
    display: flex; align-items: baseline; gap: 14px;
    border-bottom: 1px solid var(--border);
    padding-bottom: 14px; margin-bottom: 4px;
}
.case-mark { font-family: 'JetBrains Mono', monospace; font-size: 0.78rem; color: var(--text-dim); letter-spacing: 2px; }
.case-title {
    font-family: 'Space Grotesk', sans-serif; font-weight: 700; font-size: 2.1rem;
    color: var(--text); letter-spacing: -0.5px;
}
.case-sub { font-family: 'IBM Plex Sans', sans-serif; font-size: 0.95rem; color: var(--text-dim); margin-top: -6px; }

/* ── Scan target label, viewfinder-bracket motif ── */
.scan-label {
    font-family: 'JetBrains Mono', monospace; font-size: 0.8rem; letter-spacing: 3px;
    color: var(--text-dim); text-transform: uppercase; margin-bottom: 8px;
    display: flex; align-items: center; gap: 10px;
}
.scan-label .bracket { color: var(--amber); font-size: 1rem; }

/* ── Textarea (the "scan target") ── */
.stTextArea textarea {
    font-family: 'JetBrains Mono', monospace !important;
    background-color: var(--surface-deep) !important;
    color: #C9D1D9 !important;
    border: 1px solid var(--border) !important;
    border-radius: 4px !important;
}
.stTextArea textarea:focus {
    border-color: var(--amber) !important;
    box-shadow: 0 0 0 1px var(--amber) !important;
}

/* ── Buttons ── */
.stButton>button {
    background: var(--amber) !important;
    color: #15171C !important;
    border: none !important;
    border-radius: 4px !important;
    font-family: 'JetBrains Mono', monospace !important;
    font-weight: 700 !important;
    letter-spacing: 1.5px !important;
    text-transform: uppercase;
    font-size: 0.82rem !important;
    padding: 0.7rem !important;
    width: 100%;
    transition: filter 0.15s ease;
}
.stButton>button:hover { filter: brightness(1.12); }

button[kind="secondary"] {
    background: transparent !important;
    color: var(--text-dim) !important;
    border: 1px solid var(--border) !important;
}

/* ── Stamp badge — signature element ── */
@keyframes stampDown {
    0%   { transform: scale(2.2) rotate(-18deg); opacity: 0; }
    60%  { transform: scale(0.92) rotate(-7deg); opacity: 1; }
    100% { transform: scale(1) rotate(-8deg); opacity: 1; }
}
.stamp-wrap { display: flex; justify-content: center; margin: 1.5rem 0; }
.stamp {
    font-family: 'JetBrains Mono', monospace;
    font-weight: 700; font-size: 1.15rem; letter-spacing: 3px;
    border: 3px double; border-radius: 50%;
    width: 168px; height: 168px;
    display: flex; align-items: center; justify-content: center; text-align: center;
    transform: rotate(-8deg);
    animation: stampDown 0.5s ease-out;
    line-height: 1.3;
}
.stamp-flagged { color: var(--amber); border-color: var(--amber); background: var(--amber-soft); }
.stamp-secure  { color: var(--teal); border-color: var(--teal); background: var(--teal-soft); }

/* ── Risk score panel ── */
.risk-panel {
    border: 1px solid var(--border); border-radius: 6px; padding: 1.2rem 1.5rem;
    background: var(--surface); display: flex; align-items: center; gap: 1.2rem;
    margin-bottom: 1.2rem;
}
.risk-num { font-family: 'Space Grotesk', sans-serif; font-weight: 700; font-size: 2.6rem; line-height: 1; }
.risk-label { font-family: 'JetBrains Mono', monospace; font-size: 0.72rem; letter-spacing: 2px; color: var(--text-dim); text-transform: uppercase; }
.risk-level { font-family: 'Space Grotesk', sans-serif; font-weight: 700; font-size: 1.05rem; }

/* ── Vulnerability cards ── */
.vuln-card {
    border-left: 3px solid var(--border); background: var(--surface);
    border-radius: 4px; padding: 1rem 1.3rem; margin-bottom: 10px;
}
.vuln-card.sev-critical { border-left-color: var(--amber); }
.vuln-card.sev-high     { border-left-color: var(--orange); }
.vuln-card.sev-medium   { border-left-color: var(--yellow); }
.vuln-card.sev-low      { border-left-color: var(--teal); }

.vuln-top { display: flex; align-items: center; gap: 10px; margin-bottom: 8px; flex-wrap: wrap; }
.sev-badge {
    font-family: 'JetBrains Mono', monospace; font-size: 0.68rem; font-weight: 700;
    letter-spacing: 1px; padding: 3px 9px; border-radius: 3px; text-transform: uppercase;
}
.sev-critical .sev-badge { background: var(--amber-soft); color: var(--amber); }
.sev-high .sev-badge     { background: var(--orange-soft); color: var(--orange); }
.sev-medium .sev-badge   { background: var(--yellow-soft); color: var(--yellow); }
.sev-low .sev-badge      { background: var(--teal-soft); color: var(--teal); }

.owasp-tag { font-family: 'JetBrains Mono', monospace; font-size: 0.72rem; color: var(--text-dim); }
.vuln-title { font-family: 'Space Grotesk', sans-serif; font-weight: 700; font-size: 1rem; color: var(--text); }
.vuln-body p { font-size: 0.88rem; color: var(--text-dim); line-height: 1.6; margin: 4px 0; }
.vuln-body b { color: var(--text); }

/* ── Verification table ── */
.stMarkdown table { border-collapse: collapse; width: 100%; }
.stMarkdown table th { font-family: 'JetBrains Mono', monospace; font-size: 0.72rem; letter-spacing: 1px; text-transform: uppercase; color: var(--text-dim); border-bottom: 1px solid var(--border); padding: 8px; text-align: left; }
.stMarkdown table td { padding: 8px; border-bottom: 1px solid var(--border); font-size: 0.88rem; }

/* ── Empty / idle state ── */
.idle-frame {
    border: 1px dashed var(--border); border-radius: 6px; padding: 3rem 2rem;
    text-align: center; color: var(--text-dim);
}
.idle-frame .glyph { font-size: 1.6rem; color: var(--amber); margin-bottom: 0.6rem; }

/* misc */
hr { border-color: var(--border) !important; }
</style>
""", unsafe_allow_html=True)

# ═════════════════════════════════════════════════════════════════════════════
# HAND-BUILT SVG GRAPHICS — simple safe primitives, no external image deps
# ═════════════════════════════════════════════════════════════════════════════
SVG_GRID_BG = """
<svg style="position:fixed;top:0;left:0;width:100%;height:100%;z-index:0;pointer-events:none;opacity:0.05;" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <pattern id="dossierGrid" width="40" height="40" patternUnits="userSpaceOnUse">
      <path d="M 40 0 L 0 0 0 40" fill="none" stroke="#E2572B" stroke-width="1"/>
    </pattern>
  </defs>
  <rect width="100%" height="100%" fill="url(#dossierGrid)" />
</svg>
"""

SVG_SHIELD_HERO = """
<svg width="52" height="52" viewBox="0 0 64 64" xmlns="http://www.w3.org/2000/svg">
  <polygon points="8,14 56,14 56,30 32,60 8,30" fill="none" stroke="#E2572B" stroke-width="2.5"/>
  <line x1="14" y1="24" x2="50" y2="24" stroke="#E2572B" stroke-width="1.2" opacity="0.6"/>
  <line x1="14" y1="34" x2="44" y2="34" stroke="#E2572B" stroke-width="1.2" opacity="0.6"/>
  <circle cx="20" cy="24" r="2.2" fill="#E2572B"/>
  <circle cx="44" cy="34" r="2.2" fill="#E2572B"/>
</svg>
"""

SVG_EMPTY_FOLDER = """
<svg width="48" height="48" viewBox="0 0 64 64" xmlns="http://www.w3.org/2000/svg" style="margin-bottom:6px;">
  <rect x="8" y="20" width="48" height="32" rx="3" fill="none" stroke="#9CA0AC" stroke-width="2"/>
  <rect x="8" y="14" width="22" height="8" rx="2" fill="none" stroke="#9CA0AC" stroke-width="2"/>
  <circle cx="42" cy="38" r="9" fill="none" stroke="#E2572B" stroke-width="2.5"/>
  <line x1="48" y1="44" x2="56" y2="52" stroke="#E2572B" stroke-width="2.5" stroke-linecap="round"/>
</svg>
"""

SVG_RADAR_SCAN = """
<style>
@keyframes radarSpin { from { transform: rotate(0deg); } to { transform: rotate(360deg); } }
.radar-sweep { transform-origin: 32px 32px; animation: radarSpin 1.1s linear infinite; }
</style>
<div style="display:flex;justify-content:center;padding:1rem;">
<svg width="72" height="72" viewBox="0 0 64 64">
  <circle cx="32" cy="32" r="28" fill="none" stroke="#2C2F38" stroke-width="2"/>
  <circle cx="32" cy="32" r="18" fill="none" stroke="#2C2F38" stroke-width="1"/>
  <circle cx="32" cy="32" r="8" fill="none" stroke="#2C2F38" stroke-width="1"/>
  <line class="radar-sweep" x1="32" y1="32" x2="32" y2="6" stroke="#E2572B" stroke-width="2"/>
</svg>
</div>
"""

def sev_icon():
    return ('<svg width="13" height="13" viewBox="0 0 24 24" style="vertical-align:-2px;margin-right:2px;">'
            '<polygon points="12,3 22,20 2,20" fill="none" stroke="currentColor" stroke-width="2"/>'
            '<line x1="12" y1="9" x2="12" y2="14" stroke="currentColor" stroke-width="2"/>'
            '<circle cx="12" cy="17" r="1" fill="currentColor"/></svg>')

# ═════════════════════════════════════════════════════════════════════════════
# MODELS
# ═════════════════════════════════════════════════════════════════════════════
MODEL_OPTIONS = {
    "Llama 3.1 8B — Fast":    "llama-3.1-8b-instant",
    "Llama 3.3 70B — Deep":   "llama-3.3-70b-versatile",
    "Gemma2 9B — Fallback":   "gemma2-9b-it",
}

# ═════════════════════════════════════════════════════════════════════════════
# PROMPTS
# ═════════════════════════════════════════════════════════════════════════════
AUDIT_PROMPT = """You are OnyxSec's Auditor. Analyze the given code against the OWASP Top 10
and report every flaw clearly. You NEVER write a full corrected/rewritten version of the code —
your job is to find and explain, not to fix it. The person must write their own fix.

OWASP TOP 10 — check every category:
A01 Broken Access Control · A02 Cryptographic Failures · A03 Injection ·
A04 Insecure Design · A05 Security Misconfiguration · A06 Vulnerable & Outdated Components ·
A07 Auth & Session Failures · A08 Software Integrity Failures ·
A09 Security Logging Failures · A10 SSRF

For EVERY vulnerability found, output exactly this block (no deviation):

### [SEVERITY] | A0X — Category Name
**Where:** describe or quote the relevant part of the code
**Risk:** what an attacker could actually do because of this
**What to research/use:** name the concept, pattern, or library category that fixes it
(e.g. "parameterized queries", "an auth middleware like Supabase auth-helpers") —
do NOT write the actual corrected code, only point them toward the right fix.

After all findings, end with exactly:
## RISK SCORE: X/100

If there are truly zero real vulnerabilities, say so plainly and use RISK SCORE: 0/100.
Never include a full corrected code block under any circumstance in this mode."""

VERIFY_PROMPT = """You are OnyxSec's Verifier. You receive an ORIGINAL audit report and the user's
REWRITTEN code — their attempt to fix the issues themselves. Check the rewrite against every
original finding.

Output exactly this format:

## VERIFICATION RESULT
| Original Issue | Status |
|---|---|
| [short issue title] | ✅ Fixed |

(Status must be one of: ✅ Fixed · ⚠️ Partially Fixed · ❌ Still Present)

If the rewrite introduces any NEW vulnerability not in the original list, add a row with
🆕 New Issue and describe it briefly below the table.

## NEW RISK SCORE: X/100

## VERDICT
One short, direct, honest paragraph. If something is still wrong, describe the gap in plain
language — do not write the corrected code for them, describe what's missing conceptually."""

REFERENCE_PROMPT = """You are OnyxSec, asked explicitly to reveal a reference fix as a learning aid.
Given the original vulnerable code and the audit findings, write the complete, corrected,
production-ready code with every issue resolved. Output only a single clean code block,
no commentary before or after it."""


# ═════════════════════════════════════════════════════════════════════════════
# GROQ CALLS
# ═════════════════════════════════════════════════════════════════════════════
def call_groq(api_key, system_prompt, user_content, model):
    client = Groq(api_key=api_key)
    resp = client.chat.completions.create(
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_content},
        ],
        model=model,
        temperature=0.15,
        max_tokens=8192,
    )
    return resp.choices[0].message.content


def parse_risk_score(text, label="RISK SCORE"):
    match = re.search(rf"{label}:\s*(\d+)\s*/\s*100", text)
    if match:
        return min(100, max(0, int(match.group(1))))
    return None


def risk_level(score):
    if score >= 75: return ("CRITICAL", "var(--amber)")
    if score >= 50: return ("HIGH", "var(--orange)")
    if score >= 25: return ("MEDIUM", "var(--yellow)")
    return ("LOW", "var(--teal)")


def parse_vulnerabilities(audit_text):
    """Parse the strict ### [SEVERITY] | A0X — Category blocks into structured cards."""
    pattern = r"### \[(\w+)\]\s*\|\s*(A\d{2})\s*—\s*(.+?)\n(.*?)(?=\n### |\n## RISK SCORE|\Z)"
    matches = re.findall(pattern, audit_text, re.DOTALL)
    vulns = []
    for sev, owasp_id, category, body in matches:
        vulns.append({
            "severity": sev.strip().upper(),
            "owasp_id": owasp_id.strip(),
            "category": category.strip(),
            "body": body.strip(),
        })
    return vulns


def render_vuln_card(v):
    sev_class = f"sev-{v['severity'].lower()}"
    body_html = v["body"].replace("**Where:**", "<p><b>Where:</b>").replace(
        "**Risk:**", "</p><p><b>Risk:</b>").replace(
        "**What to research/use:**", "</p><p><b>Fix direction:</b>") + "</p>"
    st.markdown(f"""
    <div class="vuln-card {sev_class}">
        <div class="vuln-top">
            <span class="sev-badge">{sev_icon()}{v['severity']}</span>
            <span class="owasp-tag">{v['owasp_id']}</span>
            <span class="vuln-title">{v['category']}</span>
        </div>
        <div class="vuln-body">{body_html}</div>
    </div>
    """, unsafe_allow_html=True)


DEFAULT_CODE = """import { QueryClient } from "@tanstack/react-query";
import { createRouter } from "@tanstack/react-router";
import { routeTree } from "./routeTree.gen";

// DANGER: No authentication middleware wrapped around the router
// DANGER: API keys might be exposed in components

export const getRouter = () => {
  const queryClient = new QueryClient();

  const router = createRouter({
    routeTree,
    context: { queryClient },
    scrollRestoration: true,
    defaultPreloadStaleTime: 0,
  });

  return router;
};
"""

# ═════════════════════════════════════════════════════════════════════════════
# SESSION STATE
# ═════════════════════════════════════════════════════════════════════════════
defaults = {
    "stage": "idle",          # idle -> audited -> verified
    "case_number": 0,
    "attempt_number": 0,
    "original_code": "",
    "audit_report": "",
    "audit_score": None,
    "rewritten_code": "",
    "verify_report": "",
    "verify_score": None,
    "reference_fix": "",
}
for k, v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v

# ═════════════════════════════════════════════════════════════════════════════
# SIDEBAR
# ═════════════════════════════════════════════════════════════════════════════
with st.sidebar:
    st.markdown("##### ◆ ENGINE CONFIG")
    api_key = st.text_input("Groq API Key", type="password", help="Free at console.groq.com")
    model_label = st.selectbox("Audit Model", list(MODEL_OPTIONS.keys()), index=0)
    model = MODEL_OPTIONS[model_label]
    st.markdown("---")
    st.caption("CASE FILES OPENED: " + str(st.session_state.case_number))
    st.caption("COST PER SCAN: $0.00")
    st.markdown("---")
    if st.button("↺ Close Case & Start Over", use_container_width=True):
        for k, v in defaults.items():
            if k != "case_number":
                st.session_state[k] = v
        st.rerun()

# ═════════════════════════════════════════════════════════════════════════════
# HEADER
# ═════════════════════════════════════════════════════════════════════════════
case_id = f"{st.session_state.case_number:03d}"
st.markdown(SVG_GRID_BG, unsafe_allow_html=True)
st.markdown(f"""
<div class="case-header">
    {SVG_SHIELD_HERO}
    <span class="case-title">ONYXSEC</span>
    <span class="case-mark">CASE FILE NO. {case_id}</span>
</div>
<p class="case-sub">Security audit dossier for AI-generated code — find the flaw, fix it yourself, get verified.</p>
""", unsafe_allow_html=True)
st.write("")

# ═════════════════════════════════════════════════════════════════════════════
# STAGE 1 — SUBMIT CODE FOR AUDIT
# ═════════════════════════════════════════════════════════════════════════════
if st.session_state.stage == "idle":
    col1, col2 = st.columns([1, 1], gap="large")

    with col1:
        st.markdown('<div class="scan-label"><span class="bracket">⌐</span> TARGET CODE <span class="bracket">¬</span></div>', unsafe_allow_html=True)
        user_code = st.text_area("code", value=DEFAULT_CODE, height=420,
                                  max_chars=15000, label_visibility="collapsed")
        st.caption(f"{len(user_code):,} / 15,000 characters")
        run = st.button("OPEN CASE FILE — RUN AUDIT")

    with col2:
        st.markdown('<div class="scan-label"><span class="bracket">⌐</span> FINDINGS <span class="bracket">¬</span></div>', unsafe_allow_html=True)
        st.markdown(f"""
        <div class="idle-frame">
            {SVG_EMPTY_FOLDER}
            <b style="color:#EDEAE3;">No case open</b>
            <p style="margin-top:6px;font-size:0.85rem;">Paste code on the left and run the audit.
            OnyxSec will flag what's wrong — then it's your job to rewrite it.</p>
        </div>
        """, unsafe_allow_html=True)

    if run:
        if not api_key:
            st.error("No API key. Add your Groq key in the sidebar — free at console.groq.com")
        elif not user_code.strip():
            st.warning("Target code is empty.")
        else:
            radar = st.empty()
            radar.markdown(SVG_RADAR_SCAN, unsafe_allow_html=True)
            with st.status("Opening case file...", expanded=True) as status:
                status.update(label="Checking against OWASP Top 10...")
                try:
                    report = call_groq(api_key, AUDIT_PROMPT, f"Audit this code:\n\n```\n{user_code}\n```", model)
                    status.update(label="Case file ready.", state="complete", expanded=False)
                except Exception as e:
                    radar.empty()
                    status.update(label="Audit failed.", state="error")
                    st.error(f"Error: {e}")
                    st.stop()
            radar.empty()

            st.session_state.case_number += 1
            st.session_state.attempt_number = 0
            st.session_state.original_code = user_code
            st.session_state.audit_report = report
            st.session_state.audit_score = parse_risk_score(report, "RISK SCORE")
            st.session_state.stage = "audited"
            st.rerun()

# ═════════════════════════════════════════════════════════════════════════════
# STAGE 2 — SHOW FINDINGS, ASK USER TO REWRITE
# ═════════════════════════════════════════════════════════════════════════════
elif st.session_state.stage == "audited":
    score = st.session_state.audit_score if st.session_state.audit_score is not None else 50
    level, color = risk_level(score)

    st.markdown(f"""
    <div class="risk-panel">
        <div class="risk-num" style="color:{color}">{score}</div>
        <div>
            <div class="risk-label">Risk Score / 100</div>
            <div class="risk-level" style="color:{color}">{level} RISK</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="stamp-wrap"><div class="stamp stamp-flagged">⚠<br>FLAGGED</div></div>', unsafe_allow_html=True)

    vulns = parse_vulnerabilities(st.session_state.audit_report)
    st.markdown("##### Findings")
    if vulns:
        for v in vulns:
            render_vuln_card(v)
    else:
        st.markdown(st.session_state.audit_report)

    st.divider()
    st.markdown('<div class="scan-label"><span class="bracket">⌐</span> NOW YOU TRY — REWRITE IT <span class="bracket">¬</span></div>', unsafe_allow_html=True)
    st.caption("Use the fix directions above. No full solution is given — write your own corrected version.")

    rewrite = st.text_area("rewrite", value=st.session_state.original_code, height=320, label_visibility="collapsed")

    c1, c2, c3 = st.columns([2, 1, 1])
    with c1:
        verify_click = st.button("SUBMIT REWRITE FOR VERIFICATION")
    with c2:
        hint_click = st.button("Reveal Reference Fix", type="secondary")
    with c3:
        if st.button("Abandon Case", type="secondary"):
            st.session_state.stage = "idle"
            st.rerun()

    if hint_click:
        with st.spinner("Preparing reference fix..."):
            try:
                ref = call_groq(
                    api_key, REFERENCE_PROMPT,
                    f"Original code:\n```\n{st.session_state.original_code}\n```\n\nAudit findings:\n{st.session_state.audit_report}",
                    model
                )
                st.session_state.reference_fix = ref
            except Exception as e:
                st.error(f"Error: {e}")

    if st.session_state.reference_fix:
        with st.expander("Reference fix (use as a last resort)", expanded=True):
            st.markdown(st.session_state.reference_fix)

    if verify_click:
        if not rewrite.strip():
            st.warning("Rewrite box is empty.")
        else:
            with st.status("Checking your rewrite against original findings...", expanded=True) as status:
                try:
                    verify_input = f"ORIGINAL AUDIT REPORT:\n{st.session_state.audit_report}\n\nREWRITTEN CODE:\n```\n{rewrite}\n```"
                    vreport = call_groq(api_key, VERIFY_PROMPT, verify_input, model)
                    status.update(label="Verification complete.", state="complete", expanded=False)
                except Exception as e:
                    status.update(label="Verification failed.", state="error")
                    st.error(f"Error: {e}")
                    st.stop()

            st.session_state.attempt_number += 1
            st.session_state.rewritten_code = rewrite
            st.session_state.verify_report = vreport
            st.session_state.verify_score = parse_risk_score(vreport, "NEW RISK SCORE")
            st.session_state.stage = "verified"
            st.rerun()

# ═════════════════════════════════════════════════════════════════════════════
# STAGE 3 — VERIFICATION RESULT
# ═════════════════════════════════════════════════════════════════════════════
elif st.session_state.stage == "verified":
    score = st.session_state.verify_score if st.session_state.verify_score is not None else 50
    level, color = risk_level(score)
    fully_secure = score == 0

    st.markdown(f"""
    <div class="risk-panel">
        <div class="risk-num" style="color:{color}">{score}</div>
        <div>
            <div class="risk-label">Updated Risk Score / 100 · Attempt #{st.session_state.attempt_number}</div>
            <div class="risk-level" style="color:{color}">{level} RISK</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    if fully_secure:
        st.markdown('<div class="stamp-wrap"><div class="stamp stamp-secure">✓<br>SECURE</div></div>', unsafe_allow_html=True)
        st.balloons()
    else:
        st.markdown('<div class="stamp-wrap"><div class="stamp stamp-flagged">⚠<br>STILL FLAGGED</div></div>', unsafe_allow_html=True)

    st.markdown(st.session_state.verify_report)

    st.divider()
    c1, c2 = st.columns(2)
    with c1:
        if not fully_secure and st.button("REWRITE AGAIN"):
            st.session_state.stage = "audited"
            # keep audit_report as the original target list; carry forward rewrite as new base
            st.session_state.original_code = st.session_state.rewritten_code
            st.rerun()
    with c2:
        if st.button("CLOSE CASE & SCAN NEW CODE", type="secondary"):
            for k, v in defaults.items():
                if k != "case_number":
                    st.session_state[k] = v
            st.session_state.stage = "idle"
            st.rerun()

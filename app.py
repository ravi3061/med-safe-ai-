"""
MedSafe AI — Intelligent Healthcare Assistance Platform
Main Streamlit application with premium UI, sidebar navigation, and multi-page routing.
"""
import streamlit as st

# ═══════════════════════════════════════
# Page configuration - MUST be first
# ═══════════════════════════════════════
st.set_page_config(
    page_title="MedSafe AI — Healthcare Assistant",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ═══════════════════════════════════════
# Home Page
# ═══════════════════════════════════════
def render_home():
    """Render the home / landing page."""
    # Hero section
    st.markdown("""
    <div class="hero-section">
        <div class="hero-badge">🧬 AI-Powered Healthcare Safety</div>
        <div class="hero-title">MedSafe AI</div>
        <div class="hero-subtitle">
            Your intelligent companion for medicine safety awareness, symptom understanding, 
            and early risk identification
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Stats
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown("""
        <div class="stat-card">
            <div class="stat-number">115+</div>
            <div class="stat-label">Medicines in Database</div>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown("""
        <div class="stat-card">
            <div class="stat-number">80+</div>
            <div class="stat-label">Drug Interactions</div>
        </div>
        """, unsafe_allow_html=True)
    with col3:
        st.markdown("""
        <div class="stat-card">
            <div class="stat-number">55+</div>
            <div class="stat-label">Symptoms Covered</div>
        </div>
        """, unsafe_allow_html=True)
    with col4:
        st.markdown("""
        <div class="stat-card">
            <div class="stat-number">5</div>
            <div class="stat-label">Smart Modules</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Feature cards
    st.markdown("## 🧩 Platform Modules")
    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("""
        <div class="feature-card" style="--card-accent: linear-gradient(90deg, #0ea5e9, #38bdf8);">
            <span class="feature-icon">💊</span>
            <div class="feature-title">Medicine Interaction Checker</div>
            <div class="feature-desc">
                Select multiple medicines and instantly check for known drug-drug interactions. 
                Powered by fuzzy matching and AI-generated safety notes.
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class="feature-card" style="--card-accent: linear-gradient(90deg, #f59e0b, #fbbf24);">
            <span class="feature-icon">📝</span>
            <div class="feature-title">Side-Effect Monitor</div>
            <div class="feature-desc">
                Log your post-medication experiences including age, dosage, and symptoms. 
                Receive AI-powered educational insights about contributing factors.
            </div>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class="feature-card" style="--card-accent: linear-gradient(90deg, #8b5cf6, #a78bfa);">
            <span class="feature-icon">📄</span>
            <div class="feature-title">Prescription Analyzer</div>
            <div class="feature-desc">
                Upload a prescription image and let AI extract medicine names, active salts, 
                dosages, and frequencies in a structured format.
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class="feature-card" style="--card-accent: linear-gradient(90deg, #ef4444, #f87171);">
            <span class="feature-icon">🚨</span>
            <div class="feature-title">Emergency Risk Predictor</div>
            <div class="feature-desc">
                Assess symptom urgency with transparent rule-based risk scoring. 
                Get color-coded risk levels with clear next-step guidance.
            </div>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown("""
        <div class="feature-card" style="--card-accent: linear-gradient(90deg, #10b981, #34d399);">
            <span class="feature-icon">🩺</span>
            <div class="feature-title">Symptom & Doubt Solver</div>
            <div class="feature-desc">
                Get structured guidance on symptoms including home remedies, yoga exercises, 
                dietary tips, and warning signs to watch for.
            </div>
        </div>
        """, unsafe_allow_html=True)

        # How it works card
        st.markdown("""
        <div class="feature-card" style="--card-accent: linear-gradient(90deg, #06b6d4, #67e8f9);">
            <span class="feature-icon">⚡</span>
            <div class="feature-title">How It Works</div>
            <div class="feature-desc">
                <strong>1.</strong> Select a module from the sidebar<br>
                <strong>2.</strong> Enter your data or upload an image<br>
                <strong>3.</strong> Get instant educational insights<br>
                <strong>4.</strong> Add API key for AI-enhanced analysis
            </div>
        </div>
        """, unsafe_allow_html=True)

    # Tech stack
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("## 🔧 Technology Stack")
    tech_cols = st.columns(5)
    techs = [
        ("🖥️", "Streamlit", "Interactive UI"),
        ("🧠", "Google Gemini", "LLM & Vision AI"),
        ("🔍", "RapidFuzz", "Fuzzy Matching"),
        ("📊", "Pandas", "Data Processing"),
        ("🖼️", "Pillow", "Image Processing"),
    ]
    for col, (icon, name, desc) in zip(tech_cols, techs):
        with col:
            st.markdown(f"""
            <div class="stat-card">
                <div style="font-size:2rem; margin-bottom:0.3rem;">{icon}</div>
                <div style="font-weight:700; color:#e2e8f0; font-size:0.95rem;">{name}</div>
                <div style="font-size:0.8rem; color:#64748b;">{desc}</div>
            </div>
            """, unsafe_allow_html=True)

    # Disclaimer
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("""
    <div class="disclaimer">
        ⚕️ <strong>Important Disclaimer:</strong> MedSafe AI is an educational health awareness platform. 
        It does <strong>not</strong> provide medical diagnoses, prescriptions, or treatment recommendations. 
        All information is for educational purposes only. Always consult qualified healthcare professionals 
        for medical advice. In case of a medical emergency, call emergency services immediately.
    </div>
    """, unsafe_allow_html=True)


# ═══════════════════════════════════════
# Premium CSS Styling
# ═══════════════════════════════════════
st.markdown("""
<style>
/* ═══════════════ IMPORTS ═══════════════ */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

/* ═══════════════ GLOBAL ═══════════════ */
* { font-family: 'Inter', sans-serif; }

.stApp {
    background: linear-gradient(135deg, #0f172a 0%, #1a1a2e 50%, #0f172a 100%);
}

/* ═══════════════ SIDEBAR ═══════════════ */
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0c1222 0%, #1a1a2e 100%) !important;
    border-right: 1px solid rgba(14, 165, 233, 0.15);
}

section[data-testid="stSidebar"] .stRadio > label {
    font-size: 0.9rem;
    font-weight: 500;
    color: #94a3b8;
}

section[data-testid="stSidebar"] .stRadio > div > label {
    padding: 12px 16px !important;
    border-radius: 12px !important;
    margin-bottom: 4px !important;
    transition: all 0.3s ease !important;
    border: 1px solid transparent !important;
}

section[data-testid="stSidebar"] .stRadio > div > label:hover {
    background: rgba(14, 165, 233, 0.1) !important;
    border-color: rgba(14, 165, 233, 0.2) !important;
}

/* ═══════════════ PAGE HEADER ═══════════════ */
.page-header {
    text-align: center;
    padding: 2rem 1rem 1.5rem;
    margin-bottom: 1.5rem;
    background: linear-gradient(135deg, rgba(14, 165, 233, 0.08) 0%, rgba(139, 92, 246, 0.08) 100%);
    border-radius: 20px;
    border: 1px solid rgba(14, 165, 233, 0.15);
    backdrop-filter: blur(10px);
}

.page-header h1 {
    font-size: 2.2rem;
    font-weight: 800;
    background: linear-gradient(135deg, #0ea5e9, #8b5cf6);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    margin-bottom: 0.5rem;
}

.page-header .subtitle {
    color: #94a3b8;
    font-size: 1.05rem;
    font-weight: 300;
}

/* ═══════════════ HERO SECTION ═══════════════ */
.hero-section {
    text-align: center;
    padding: 3rem 2rem;
    background: linear-gradient(135deg, rgba(14, 165, 233, 0.06) 0%, rgba(139, 92, 246, 0.06) 50%, rgba(6, 182, 212, 0.06) 100%);
    border-radius: 24px;
    border: 1px solid rgba(14, 165, 233, 0.12);
    margin-bottom: 2rem;
    position: relative;
    overflow: hidden;
}

.hero-section::before {
    content: '';
    position: absolute;
    top: -50%;
    left: -50%;
    width: 200%;
    height: 200%;
    background: radial-gradient(circle, rgba(14, 165, 233, 0.03) 0%, transparent 50%);
    animation: pulse-glow 6s ease-in-out infinite;
}

@keyframes pulse-glow {
    0%, 100% { opacity: 0.5; transform: scale(1); }
    50% { opacity: 1; transform: scale(1.05); }
}

.hero-title {
    font-size: 3rem;
    font-weight: 800;
    background: linear-gradient(135deg, #0ea5e9, #06b6d4, #8b5cf6);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    margin-bottom: 0.5rem;
    position: relative;
    z-index: 1;
}

.hero-subtitle {
    font-size: 1.2rem;
    color: #94a3b8;
    font-weight: 300;
    max-width: 600px;
    margin: 0 auto 1.5rem;
    position: relative;
    z-index: 1;
}

.hero-badge {
    display: inline-block;
    background: linear-gradient(135deg, rgba(14, 165, 233, 0.15), rgba(139, 92, 246, 0.15));
    border: 1px solid rgba(14, 165, 233, 0.3);
    border-radius: 100px;
    padding: 8px 20px;
    font-size: 0.85rem;
    color: #7dd3fc;
    font-weight: 500;
    position: relative;
    z-index: 1;
    margin-bottom: 1rem;
}

/* ═══════════════ FEATURE CARDS ═══════════════ */
.feature-card {
    background: linear-gradient(135deg, rgba(30, 41, 59, 0.7) 0%, rgba(30, 41, 59, 0.4) 100%);
    border: 1px solid rgba(14, 165, 233, 0.12);
    border-radius: 16px;
    padding: 1.8rem;
    margin-bottom: 1rem;
    transition: all 0.3s ease;
    backdrop-filter: blur(10px);
    position: relative;
    overflow: hidden;
}

.feature-card::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    height: 3px;
    background: var(--card-accent, linear-gradient(90deg, #0ea5e9, #06b6d4));
    border-radius: 16px 16px 0 0;
}

.feature-card:hover {
    border-color: rgba(14, 165, 233, 0.3);
    transform: translateY(-2px);
    box-shadow: 0 8px 32px rgba(14, 165, 233, 0.12);
}

.feature-icon {
    font-size: 2.5rem;
    margin-bottom: 0.8rem;
    display: block;
}

.feature-title {
    font-size: 1.2rem;
    font-weight: 700;
    color: #e2e8f0;
    margin-bottom: 0.5rem;
}

.feature-desc {
    font-size: 0.9rem;
    color: #94a3b8;
    line-height: 1.6;
}

/* ═══════════════ INFO/WARNING BANNERS ═══════════════ */
.info-banner {
    background: rgba(14, 165, 233, 0.08);
    border: 1px solid rgba(14, 165, 233, 0.2);
    border-radius: 12px;
    padding: 1rem 1.2rem;
    margin-bottom: 1.5rem;
    display: flex;
    align-items: flex-start;
    gap: 12px;
    font-size: 0.9rem;
    color: #7dd3fc;
}

.warning-banner {
    background: rgba(245, 158, 11, 0.08);
    border: 1px solid rgba(245, 158, 11, 0.2);
    border-radius: 12px;
    padding: 1rem 1.2rem;
    margin-bottom: 1.5rem;
    display: flex;
    align-items: flex-start;
    gap: 12px;
    font-size: 0.9rem;
    color: #fbbf24;
}

.info-icon, .warning-icon {
    font-size: 1.3rem;
    flex-shrink: 0;
}

/* ═══════════════ MEDICINE CARDS ═══════════════ */
.med-card {
    background: rgba(30, 41, 59, 0.6);
    border: 1px solid rgba(14, 165, 233, 0.15);
    border-radius: 12px;
    padding: 1.2rem;
    margin-bottom: 0.8rem;
    transition: all 0.2s ease;
}

.med-card:hover { border-color: rgba(14, 165, 233, 0.3); }

.med-name {
    font-size: 1.1rem;
    font-weight: 700;
    color: #e2e8f0;
    margin-bottom: 0.6rem;
}

.med-salt, .med-category, .med-use {
    font-size: 0.85rem;
    color: #94a3b8;
    margin-bottom: 0.3rem;
}

/* ═══════════════ MATCH CARDS ═══════════════ */
.match-card {
    display: flex;
    align-items: center;
    gap: 12px;
    background: rgba(30, 41, 59, 0.5);
    border: 1px solid rgba(14, 165, 233, 0.1);
    border-radius: 10px;
    padding: 10px 16px;
    margin-bottom: 6px;
}

.match-name { font-weight: 600; color: #e2e8f0; }
.match-salt { color: #64748b; font-size: 0.85rem; }
.match-score { font-weight: 700; font-size: 0.85rem; margin-left: auto; }

/* ═══════════════ INTERACTION CARDS ═══════════════ */
.interaction-card {
    border-radius: 12px;
    padding: 1.2rem 1.5rem;
    margin-bottom: 1rem;
    transition: all 0.2s ease;
}

.interaction-card:hover { transform: translateX(4px); }

.interaction-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 0.6rem;
    flex-wrap: wrap;
    gap: 8px;
}

.interaction-drugs {
    font-size: 1.05rem;
    font-weight: 700;
    color: #e2e8f0;
}

.severity-badge {
    display: inline-block;
    padding: 4px 14px;
    border-radius: 100px;
    font-size: 0.75rem;
    font-weight: 700;
    color: white;
    letter-spacing: 0.5px;
}

.interaction-desc {
    font-size: 0.9rem;
    color: #cbd5e1;
    line-height: 1.6;
}

/* ═══════════════ PRESCRIPTION CARDS ═══════════════ */
.prescription-card {
    background: rgba(30, 41, 59, 0.6);
    border: 1px solid rgba(14, 165, 233, 0.15);
    border-radius: 14px;
    padding: 1.5rem;
    margin-bottom: 1rem;
    transition: all 0.2s ease;
}

.rx-number {
    font-size: 0.8rem;
    font-weight: 700;
    color: #0ea5e9;
    text-transform: uppercase;
    letter-spacing: 1px;
    margin-bottom: 0.3rem;
}

.rx-name {
    font-size: 1.25rem;
    font-weight: 700;
    color: #e2e8f0;
    margin-bottom: 1rem;
}

.rx-details {
    display: flex;
    flex-wrap: wrap;
    gap: 12px;
}

.rx-detail {
    font-size: 0.85rem;
    color: #94a3b8;
    background: rgba(15, 23, 42, 0.5);
    padding: 6px 12px;
    border-radius: 8px;
    border: 1px solid rgba(14, 165, 233, 0.08);
}

/* ═══════════════ SYMPTOM RESULT CARDS ═══════════════ */
.symptom-result-card {
    border-radius: 12px;
    padding: 1rem 1.4rem;
    margin-bottom: 0.8rem;
}

.symptom-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
}

.symptom-header h3 {
    margin: 0;
    color: #e2e8f0;
    font-size: 1.15rem;
}

.risk-badge {
    display: inline-block;
    padding: 4px 14px;
    border-radius: 100px;
    font-size: 0.7rem;
    font-weight: 700;
    color: white;
    letter-spacing: 0.5px;
}

/* ═══════════════ RISK SCORE DISPLAY ═══════════════ */
.risk-hero {
    text-align: center;
    padding: 2rem;
    border-radius: 20px;
    background: rgba(30, 41, 59, 0.5);
    margin-bottom: 1.5rem;
    backdrop-filter: blur(10px);
}

.risk-score-display {
    display: flex;
    align-items: baseline;
    justify-content: center;
    gap: 4px;
    margin-bottom: 0.8rem;
}

.risk-score-number {
    font-size: 5rem;
    font-weight: 800;
    line-height: 1;
}

.risk-score-label {
    font-size: 1.5rem;
    color: #64748b;
    font-weight: 300;
}

.risk-urgency {
    font-size: 1.3rem;
    font-weight: 700;
}

/* ═══════════════ RISK GAUGE ═══════════════ */
.risk-gauge-container { margin-bottom: 1.5rem; }

.risk-gauge-track {
    width: 100%;
    height: 14px;
    background: rgba(30, 41, 59, 0.8);
    border-radius: 100px;
    overflow: hidden;
    border: 1px solid rgba(14, 165, 233, 0.1);
}

.risk-gauge-fill {
    height: 100%;
    border-radius: 100px;
    transition: width 1s ease-out;
}

.risk-gauge-labels {
    display: flex;
    justify-content: space-between;
    margin-top: 6px;
    font-size: 0.75rem;
    font-weight: 500;
}

/* ═══════════════ SCORE BREAKDOWN ═══════════════ */
.score-breakdown-item {
    display: flex;
    align-items: center;
    gap: 12px;
    margin-bottom: 8px;
}

.score-symptom {
    width: 200px;
    font-size: 0.85rem;
    color: #cbd5e1;
    flex-shrink: 0;
}

.score-bar-container {
    flex: 1;
    height: 8px;
    background: rgba(30, 41, 59, 0.6);
    border-radius: 100px;
    overflow: hidden;
}

.score-bar {
    height: 100%;
    border-radius: 100px;
    transition: width 0.8s ease-out;
}

.score-value {
    width: 40px;
    text-align: right;
    font-weight: 700;
    font-size: 0.85rem;
    flex-shrink: 0;
}

/* ═══════════════ GUIDANCE CARD ═══════════════ */
.guidance-card {
    background: rgba(30, 41, 59, 0.5);
    border-radius: 12px;
    padding: 1.5rem;
    margin-bottom: 1.5rem;
}

.guidance-header {
    font-size: 1.1rem;
    font-weight: 700;
    color: #e2e8f0;
    margin-bottom: 0.6rem;
}

.guidance-text {
    font-size: 0.95rem;
    color: #cbd5e1;
    line-height: 1.7;
}

/* ═══════════════ AI RESPONSE CARD ═══════════════ */
.ai-response-card {
    background: linear-gradient(135deg, rgba(139, 92, 246, 0.06) 0%, rgba(14, 165, 233, 0.06) 100%);
    border: 1px solid rgba(139, 92, 246, 0.15);
    border-radius: 16px;
    padding: 1.5rem;
    margin-bottom: 1rem;
}

.ai-header {
    font-size: 1rem;
    font-weight: 700;
    color: #c4b5fd;
    margin-bottom: 0.8rem;
    display: flex;
    align-items: center;
    gap: 8px;
}

.ai-content {
    font-size: 0.9rem;
    color: #cbd5e1;
    line-height: 1.8;
}

/* ═══════════════ SUCCESS CARD ═══════════════ */
.success-card {
    background: rgba(16, 185, 129, 0.08);
    border: 1px solid rgba(16, 185, 129, 0.2);
    border-radius: 14px;
    padding: 1.5rem;
    display: flex;
    align-items: flex-start;
    gap: 16px;
}

.success-icon { font-size: 2rem; }

.success-text {
    font-size: 0.95rem;
    color: #6ee7b7;
    line-height: 1.6;
}

/* ═══════════════ SUMMARY CARD ═══════════════ */
.summary-card {
    background: rgba(30, 41, 59, 0.5);
    border: 1px solid rgba(14, 165, 233, 0.12);
    border-radius: 14px;
    padding: 1.5rem;
    margin-top: 1rem;
    color: #cbd5e1;
    font-size: 0.9rem;
    line-height: 1.7;
}

/* ═══════════════ EMERGENCY CARD ═══════════════ */
.emergency-card {
    background: rgba(239, 68, 68, 0.06);
    border: 1px solid rgba(239, 68, 68, 0.15);
    border-radius: 14px;
    padding: 1.5rem;
    text-align: center;
    transition: all 0.2s ease;
}

.emergency-card:hover { border-color: rgba(239, 68, 68, 0.35); }

.emergency-number {
    font-size: 1.6rem;
    font-weight: 800;
    color: #fca5a5;
    margin-bottom: 0.3rem;
}

.emergency-label {
    font-size: 0.8rem;
    color: #94a3b8;
    font-weight: 500;
}

/* ═══════════════ DISCLAIMER ═══════════════ */
.disclaimer {
    background: rgba(30, 41, 59, 0.4);
    border: 1px solid rgba(245, 158, 11, 0.15);
    border-radius: 12px;
    padding: 1rem 1.4rem;
    font-size: 0.82rem;
    color: #94a3b8;
    line-height: 1.6;
    margin-top: 1rem;
}

/* ═══════════════ STAT CARD ═══════════════ */
.stat-card {
    background: rgba(30, 41, 59, 0.5);
    border: 1px solid rgba(14, 165, 233, 0.1);
    border-radius: 14px;
    padding: 1.5rem;
    text-align: center;
    transition: all 0.3s ease;
}

.stat-card:hover {
    border-color: rgba(14, 165, 233, 0.25);
    transform: translateY(-2px);
}

.stat-number {
    font-size: 2.2rem;
    font-weight: 800;
    background: linear-gradient(135deg, #0ea5e9, #06b6d4);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}

.stat-label {
    font-size: 0.85rem;
    color: #64748b;
    font-weight: 500;
    margin-top: 0.3rem;
}

/* ═══════════════ BUTTONS ═══════════════ */
.stButton > button[kind="primary"] {
    background: linear-gradient(135deg, #0ea5e9, #0284c7) !important;
    border: none !important;
    padding: 0.7rem 2rem !important;
    font-weight: 600 !important;
    border-radius: 12px !important;
    transition: all 0.3s ease !important;
    font-size: 1rem !important;
}

.stButton > button[kind="primary"]:hover {
    transform: translateY(-1px) !important;
    box-shadow: 0 6px 24px rgba(14, 165, 233, 0.3) !important;
}

/* ═══════════════ SIDEBAR BRANDING ═══════════════ */
.sidebar-brand {
    text-align: center;
    padding: 1.2rem 0.5rem;
    margin-bottom: 0.5rem;
}

.sidebar-logo {
    font-size: 2rem;
    margin-bottom: 0.4rem;
}

.sidebar-title {
    font-size: 1.5rem;
    font-weight: 800;
    background: linear-gradient(135deg, #0ea5e9, #06b6d4);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}

.sidebar-version {
    font-size: 0.7rem;
    color: #475569;
    margin-top: 0.2rem;
}

.sidebar-divider {
    border: none;
    border-top: 1px solid rgba(14, 165, 233, 0.1);
    margin: 0.8rem 0;
}

/* ═══════════════ TABS ═══════════════ */
.stTabs [data-baseweb="tab-list"] {
    gap: 2px;
    background: rgba(30, 41, 59, 0.4);
    border-radius: 12px;
    padding: 4px;
}

.stTabs [data-baseweb="tab"] {
    border-radius: 10px !important;
    padding: 8px 16px !important;
    font-size: 0.85rem !important;
}

/* ═══════════════ MULTISELECT ═══════════════ */
.stMultiSelect [data-baseweb="tag"] {
    background: rgba(14, 165, 233, 0.15) !important;
    border: 1px solid rgba(14, 165, 233, 0.3) !important;
    border-radius: 8px !important;
}

/* ═══════════════ HIDE STREAMLIT DEFAULTS ═══════════════ */
#MainMenu { visibility: hidden; }
footer { visibility: hidden; }
header { visibility: hidden; }
</style>
""", unsafe_allow_html=True)


# ═══════════════════════════════════════
# Sidebar
# ═══════════════════════════════════════
with st.sidebar:
    st.markdown("""
    <div class="sidebar-brand">
        <div class="sidebar-logo">🏥</div>
        <div class="sidebar-title">MedSafe AI</div>
        <div class="sidebar-version">v1.0 — Healthcare Assistant</div>
    </div>
    <hr class="sidebar-divider">
    """, unsafe_allow_html=True)

    page = st.radio(
        "Navigation",
        [
            "🏠 Home",
            "💊 Interaction Checker",
            "📄 Prescription Analyzer",
            "🩺 Symptom Solver",
            "📝 Side-Effect Monitor",
            "🚨 Emergency Predictor",
        ],
        label_visibility="collapsed",
    )

    st.markdown('<hr class="sidebar-divider">', unsafe_allow_html=True)

    # API Key input
    st.markdown("### 🔑 AI Configuration")
    api_key = st.text_input(
        "Gemini API Key",
        type="password",
        placeholder="Enter your API key...",
        help="Required for AI-powered features (summaries, OCR, guidance)",
    )
    if api_key:
        st.session_state["gemini_api_key"] = api_key
        st.success("✅ API key set!", icon="🔑")
    elif "gemini_api_key" not in st.session_state:
        st.session_state["gemini_api_key"] = ""

    st.markdown('<hr class="sidebar-divider">', unsafe_allow_html=True)
    st.markdown("""
    <div style="text-align:center; font-size:0.7rem; color:#475569; padding:0.5rem;">
        ⚕️ Educational Use Only<br>
        Not a Medical Device<br><br>
        Built with ❤️ using Streamlit
    </div>
    """, unsafe_allow_html=True)


# ═══════════════════════════════════════
# Page Routing
# ═══════════════════════════════════════
if page == "🏠 Home":
    render_home()
elif page == "💊 Interaction Checker":
    from modules.interaction_checker import render
    render()
elif page == "📄 Prescription Analyzer":
    from modules.prescription_analyzer import render
    render()
elif page == "🩺 Symptom Solver":
    from modules.symptom_solver import render
    render()
elif page == "📝 Side-Effect Monitor":
    from modules.side_effect_monitor import render
    render()
elif page == "🚨 Emergency Predictor":
    from modules.emergency_predictor import render
    render()

"""
Emergency Risk Predictor module.
Uses rule-based scoring to assess symptom urgency and provides AI-generated guidance.
"""
import streamlit as st
from utils.risk_scorer import calculate_risk_score, get_available_symptoms
from utils.ocr_helper import generate_ai_summary


def render():
    """Render the Emergency Risk Predictor page."""
    st.markdown("""
    <div class="page-header">
        <h1>🚨 Emergency Risk Predictor</h1>
        <p class="subtitle">Assess symptom urgency with transparent risk scoring and next-step guidance</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="info-banner">
        <span class="info-icon">⚠️</span>
        <span><strong>If you are experiencing a medical emergency, call emergency services (911/112/108) immediately.</strong>
        This tool provides an educational risk assessment only and is NOT a substitute for professional medical judgment.</span>
    </div>
    """, unsafe_allow_html=True)

    available_symptoms = get_available_symptoms()

    # Symptom selection
    st.markdown("### Select Your Current Symptoms")
    selected_symptoms = st.multiselect(
        "What are you currently experiencing?",
        options=[s.title() for s in available_symptoms],
        placeholder="Start typing to search symptoms...",
        help="Select all symptoms that currently apply to you",
    )

    # Additional context
    col1, col2 = st.columns(2)
    with col1:
        age = st.number_input("Your Age", min_value=1, max_value=120, value=30, step=1)
    with col2:
        gender = st.selectbox("Gender", ["Male", "Female", "Other", "Prefer not to say"])

    additional_info = st.text_area(
        "Additional details (optional)",
        placeholder="Any other symptoms or context not listed above...",
        height=80,
    )

    if st.button("🔍 Assess Risk Level", use_container_width=True, type="primary"):
        if not selected_symptoms:
            st.error("❌ Please select at least one symptom.")
            return

        st.markdown("---")

        # Calculate risk score
        symptoms_lower = [s.lower() for s in selected_symptoms]
        result = calculate_risk_score(symptoms_lower, age=age, gender=gender)

        score = result["score"]
        urgency = result["urgency_level"]
        urgency_color = result["urgency_color"]
        urgency_emoji = result["urgency_emoji"]
        urgency_label = result["urgency_label"]

        # Risk score hero display
        st.markdown(f"""
        <div class="risk-hero" style="border: 2px solid {urgency_color};">
            <div class="risk-score-display">
                <div class="risk-score-number" style="color: {urgency_color};">{score}</div>
                <div class="risk-score-label">/ 100</div>
            </div>
            <div class="risk-urgency" style="color: {urgency_color};">
                {urgency_emoji} {urgency_label}
            </div>
        </div>
        """, unsafe_allow_html=True)

        # Risk gauge bar
        gauge_gradient = _get_gauge_gradient(score)
        st.markdown(f"""
        <div class="risk-gauge-container">
            <div class="risk-gauge-track">
                <div class="risk-gauge-fill" style="width: {min(score, 100)}%; background: {gauge_gradient};"></div>
            </div>
            <div class="risk-gauge-labels">
                <span style="color: #10b981;">Low</span>
                <span style="color: #f59e0b;">Moderate</span>
                <span style="color: #f97316;">High</span>
                <span style="color: #ef4444;">Critical</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

        # Guidance
        st.markdown(f"""
        <div class="guidance-card" style="border-left: 4px solid {urgency_color};">
            <div class="guidance-header">{urgency_emoji} Recommended Action</div>
            <div class="guidance-text">{result['guidance']}</div>
        </div>
        """, unsafe_allow_html=True)

        # Matched symptoms breakdown
        if result["matched_symptoms"]:
            st.markdown("### 📊 Risk Score Breakdown")
            st.markdown("**Symptom contributions to your risk score:**")
            for symptom, weight in result["matched_symptoms"]:
                bar_width = min(weight * 3, 100)
                bar_color = "#ef4444" if weight >= 20 else "#f97316" if weight >= 15 else "#f59e0b" if weight >= 10 else "#10b981"
                st.markdown(f"""
                <div class="score-breakdown-item">
                    <div class="score-symptom">{symptom.title()}</div>
                    <div class="score-bar-container">
                        <div class="score-bar" style="width: {bar_width}%; background: {bar_color};"></div>
                    </div>
                    <div class="score-value" style="color: {bar_color};">+{weight}</div>
                </div>
                """, unsafe_allow_html=True)

        # Risk factors
        if result["risk_factors"]:
            st.markdown("### 📋 Additional Risk Factors")
            for factor in result["risk_factors"]:
                st.markdown(f"⚠️ {factor}")

        # AI-generated explanation
        api_key = st.session_state.get("gemini_api_key", "")
        if api_key:
            st.markdown("### 🤖 AI Emergency Guidance")
            with st.spinner("Generating guidance..."):
                symptom_text = ", ".join(selected_symptoms)
                prompt = f"""You are an emergency health educator. Based on this assessment:
- Symptoms: {symptom_text}
- Risk Score: {score}/100
- Urgency Level: {urgency} ({urgency_label})
- Patient Age: {age}
- Additional info: {additional_info if additional_info else 'None'}

Provide a brief emergency guidance response:
1. **Situation Assessment** - What these symptoms together may indicate (educational only)
2. **Immediate Steps** - 2-3 things to do right now
3. **What to Tell Emergency Services** - Key information to relay if calling for help
4. **While Waiting** - What to do while waiting for medical help (if applicable)

{"IMPORTANT: Given the HIGH/CRITICAL risk level, emphasize the urgency of seeking immediate medical attention." if score >= 40 else ""}

Be clear, concise, and educational. Keep under 200 words.
End with: "⚕️ This is an educational tool only. In any medical emergency, always call emergency services."
"""
                result_ai = generate_ai_summary(prompt, api_key)
                if result_ai["success"]:
                    st.markdown(f"""
                    <div class="ai-response-card" style="border-left: 4px solid {urgency_color};">
                        <div class="ai-header">🤖 Emergency Guidance</div>
                        <div class="ai-content">{result_ai['response']}</div>
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.error(f"AI guidance unavailable: {result_ai['error']}")
        else:
            st.info("💡 Enter your Gemini API key in the sidebar for AI-powered emergency guidance.")

    # Emergency numbers
    st.markdown("---")
    st.markdown("### 📞 Emergency Contacts")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("""
        <div class="emergency-card">
            <div class="emergency-number">🇺🇸 911</div>
            <div class="emergency-label">US Emergency</div>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown("""
        <div class="emergency-card">
            <div class="emergency-number">🇮🇳 108 / 112</div>
            <div class="emergency-label">India Emergency</div>
        </div>
        """, unsafe_allow_html=True)
    with col3:
        st.markdown("""
        <div class="emergency-card">
            <div class="emergency-number">🇪🇺 112</div>
            <div class="emergency-label">EU Emergency</div>
        </div>
        """, unsafe_allow_html=True)

    # Disclaimer
    st.markdown("""
    <div class="disclaimer" style="border-color: #ef4444;">
        🚨 <strong>IMPORTANT:</strong> This risk predictor is an educational tool using rule-based scoring. 
        It is NOT a medical device and NOT a substitute for professional medical assessment. 
        If you believe you are having a medical emergency, call emergency services IMMEDIATELY. 
        Do not rely on this tool for medical decisions.
    </div>
    """, unsafe_allow_html=True)


def _get_gauge_gradient(score):
    """Return a CSS gradient for the risk gauge based on score."""
    if score < 20:
        return "linear-gradient(90deg, #10b981, #34d399)"
    elif score < 40:
        return "linear-gradient(90deg, #10b981, #f59e0b)"
    elif score < 65:
        return "linear-gradient(90deg, #10b981, #f59e0b, #f97316)"
    else:
        return "linear-gradient(90deg, #10b981, #f59e0b, #f97316, #ef4444)"

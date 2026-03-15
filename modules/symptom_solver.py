"""
Symptom & Doubt Solver module.
Provides structured guidance for symptoms using rule-based advice and AI-enhanced explanations.
"""
import os
import streamlit as st
import pandas as pd
from utils.ocr_helper import generate_ai_summary


def _load_symptoms():
    """Load the symptoms database."""
    data_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")
    return pd.read_csv(os.path.join(data_dir, "symptoms.csv"))


def render():
    """Render the Symptom & Doubt Solver page."""
    st.markdown("""
    <div class="page-header">
        <h1>🩺 Symptom & Doubt Solver</h1>
        <p class="subtitle">Get educational guidance on symptoms with home remedies, lifestyle tips, and warning signs</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="info-banner">
        <span class="info-icon">💡</span>
        <span>Select your symptoms below. We'll provide rule-based guidance from our curated database, 
        plus AI-enhanced suggestions including home remedies, breathing exercises, and dietary tips.</span>
    </div>
    """, unsafe_allow_html=True)

    symptoms_df = _load_symptoms()
    symptom_list = sorted(symptoms_df["symptom"].tolist())

    # Symptom selection
    selected_symptoms = st.multiselect(
        "Select Your Symptoms",
        options=symptom_list,
        placeholder="Start typing to search symptoms...",
        help="Select one or more symptoms for guidance",
    )

    # Additional context
    col1, col2 = st.columns(2)
    with col1:
        age = st.number_input("Your Age (optional)", min_value=1, max_value=120, value=None, step=1)
    with col2:
        duration = st.selectbox(
            "How long have you had these symptoms?",
            ["Select...", "Just started (hours)", "Few days (1-3)", "About a week",
             "More than a week", "More than a month", "Chronic / Recurring"],
        )

    free_text = st.text_area(
        "Describe your concern (optional)",
        placeholder="E.g., 'I've had a persistent headache for 3 days and it gets worse in the evening...'",
        height=100,
    )

    if selected_symptoms and st.button("🔍 Get Guidance", use_container_width=True, type="primary"):
        st.markdown("---")

        for symptom_name in selected_symptoms:
            row = symptoms_df[symptoms_df["symptom"] == symptom_name]
            if row.empty:
                continue
            row = row.iloc[0]

            risk_level = row.get("risk_level", "moderate")
            if risk_level == "critical":
                risk_color = "#ef4444"
                risk_bg = "rgba(239, 68, 68, 0.1)"
                risk_icon = "🔴"
            elif risk_level == "high":
                risk_color = "#f97316"
                risk_bg = "rgba(249, 115, 22, 0.1)"
                risk_icon = "🟠"
            elif risk_level == "moderate":
                risk_color = "#f59e0b"
                risk_bg = "rgba(245, 158, 11, 0.1)"
                risk_icon = "🟡"
            else:
                risk_color = "#10b981"
                risk_bg = "rgba(16, 185, 129, 0.1)"
                risk_icon = "🟢"

            st.markdown(f"""
            <div class="symptom-result-card" style="border-left: 4px solid {risk_color}; background: {risk_bg};">
                <div class="symptom-header">
                    <h3>{risk_icon} {symptom_name}</h3>
                    <span class="risk-badge" style="background: {risk_color};">{risk_level.upper()} RISK</span>
                </div>
            </div>
            """, unsafe_allow_html=True)

            # Tabbed content for each symptom
            tab1, tab2, tab3, tab4, tab5 = st.tabs([
                "🔎 Possible Causes",
                "🏠 Home Remedies",
                "🧘 Exercises & Yoga",
                "🥗 Lifestyle Tips",
                "⚠️ Warning Signs"
            ])

            with tab1:
                causes = str(row.get("possible_causes", "")).split(";")
                for cause in causes:
                    cause = cause.strip()
                    if cause:
                        st.markdown(f"- {cause}")

            with tab2:
                remedies = str(row.get("home_remedy", "")).split(";")
                for remedy in remedies:
                    remedy = remedy.strip()
                    if remedy:
                        st.markdown(f"✅ {remedy}")

            with tab3:
                exercises = str(row.get("yoga_or_exercise", "")).split(";")
                for exercise in exercises:
                    exercise = exercise.strip()
                    if exercise:
                        st.markdown(f"🧘 {exercise}")

            with tab4:
                tips = str(row.get("lifestyle_tip", "")).split(";")
                for tip in tips:
                    tip = tip.strip()
                    if tip:
                        st.markdown(f"💚 {tip}")

            with tab5:
                warnings = str(row.get("warning_sign", "")).split(";")
                for warning in warnings:
                    warning = warning.strip()
                    if warning:
                        st.markdown(f"🚨 {warning}")

            st.markdown("<br>", unsafe_allow_html=True)

        # AI-enhanced guidance
        api_key = st.session_state.get("gemini_api_key", "")
        if api_key:
            st.markdown("### 🤖 AI-Enhanced Guidance")
            with st.spinner("Generating personalized guidance..."):
                symptom_text = ", ".join(selected_symptoms)
                age_text = f"Age: {age}" if age else "Age: not specified"
                duration_text = f"Duration: {duration}" if duration != "Select..." else "Duration: not specified"
                concern_text = f"User's concern: {free_text}" if free_text else ""

                prompt = f"""You are a health education assistant. A user reports these symptoms: {symptom_text}.
{age_text}. {duration_text}. {concern_text}

Provide a structured educational response with these sections:
1. **Understanding Your Symptoms** - Brief explanation of what might be causing these symptoms
2. **Home Remedies** - 3-4 practical home remedies
3. **Breathing & Relaxation** - 2-3 breathing or yoga exercises that may help
4. **Dietary Suggestions** - 3-4 foods or drinks that may provide relief
5. **When to See a Doctor** - Clear warning signs that need professional attention

Keep the tone warm, educational, and non-diagnostic. Use simple language.
Do NOT diagnose or prescribe. Keep response under 300 words.
End with: "⚕️ This is educational information only. Please consult a healthcare professional for medical advice."
"""
                result = generate_ai_summary(prompt, api_key)
                if result["success"]:
                    st.markdown(f"""
                    <div class="ai-response-card">
                        <div class="ai-header">🤖 AI Health Educator</div>
                        <div class="ai-content">{result['response']}</div>
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.error(f"AI guidance unavailable: {result['error']}")
        else:
            st.info("💡 Enter your Gemini API key in the sidebar for AI-enhanced personalized guidance.")

    # Disclaimer
    st.markdown("---")
    st.markdown("""
    <div class="disclaimer">
        ⚕️ <strong>Disclaimer:</strong> This tool provides general educational information only. 
        It is not a substitute for professional medical advice, diagnosis, or treatment. 
        If you are experiencing a medical emergency, call emergency services immediately.
    </div>
    """, unsafe_allow_html=True)

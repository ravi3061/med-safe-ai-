"""
Side-Effect Monitor module.
Allows users to log post-medication experiences and receive educational analysis.
"""
import streamlit as st
from utils.fuzzy_match import get_all_medicine_names
from utils.ocr_helper import generate_ai_summary


def render():
    """Render the Side-Effect Monitor page."""
    st.markdown("""
    <div class="page-header">
        <h1>📝 Side-Effect Monitor</h1>
        <p class="subtitle">Log your post-medication experience and receive educational insights</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="info-banner">
        <span class="info-icon">📋</span>
        <span>Fill in the form below with your details and describe how you feel after taking your medicine. 
        The AI will provide educational insights about possible contributing factors and precautions.</span>
    </div>
    """, unsafe_allow_html=True)

    all_medicines = get_all_medicine_names()

    # Form
    with st.form("side_effect_form"):
        st.markdown("### 👤 Your Information")
        col1, col2, col3 = st.columns(3)
        with col1:
            age = st.number_input("Age", min_value=1, max_value=120, value=30, step=1)
        with col2:
            gender = st.selectbox("Gender", ["Male", "Female", "Other", "Prefer not to say"])
        with col3:
            weight = st.text_input("Weight (optional)", placeholder="e.g., 70 kg")

        st.markdown("### 💊 Medication Details")
        col4, col5 = st.columns(2)
        with col4:
            medicines_taken = st.multiselect(
                "Medicines Taken",
                options=all_medicines,
                placeholder="Select medicines you've taken...",
            )
        with col5:
            other_medicines = st.text_input(
                "Other Medicines (not in list)",
                placeholder="e.g., herbal supplements, OTC drugs",
            )

        col6, col7 = st.columns(2)
        with col6:
            dosage = st.text_input("Dosage", placeholder="e.g., 500mg twice daily")
        with col7:
            duration_taken = st.selectbox(
                "How long have you been taking it?",
                ["Just started (1-2 days)", "About a week", "2-4 weeks",
                 "1-3 months", "More than 3 months"],
            )

        st.markdown("### 📝 Your Experience")
        experience = st.text_area(
            "Describe how you feel after taking the medicine",
            placeholder="E.g., 'After taking the medicine for 3 days, I've noticed mild dizziness in the mornings, "
                        "some stomach discomfort after meals, and occasional drowsiness in the afternoon...'",
            height=150,
        )

        severity = st.select_slider(
            "How would you rate the severity of your experience?",
            options=["Very Mild", "Mild", "Moderate", "Significant", "Severe"],
            value="Mild",
        )

        existing_conditions = st.text_input(
            "Any pre-existing conditions? (optional)",
            placeholder="e.g., diabetes, hypertension, asthma",
        )

        submitted = st.form_submit_button(
            "🔍 Analyze My Experience",
            use_container_width=True,
            type="primary",
        )

    if submitted:
        if not medicines_taken and not other_medicines:
            st.error("❌ Please select or enter at least one medicine.")
            return
        if not experience:
            st.error("❌ Please describe your post-medication experience.")
            return

        st.markdown("---")

        # Build the list of all medicines mentioned
        all_meds = list(medicines_taken)
        if other_medicines:
            all_meds.extend([m.strip() for m in other_medicines.split(",") if m.strip()])

        api_key = st.session_state.get("gemini_api_key", "")
        if api_key:
            st.markdown("### 🤖 AI Educational Analysis")
            with st.spinner("Analyzing your experience..."):
                prompt = f"""You are a medication safety educator providing educational insights about a user's 
post-medication experience. This is NOT medical advice or diagnosis.

**Patient Profile:**
- Age: {age}
- Gender: {gender}
- Weight: {weight if weight else 'Not specified'}
- Pre-existing conditions: {existing_conditions if existing_conditions else 'None specified'}

**Medication Details:**
- Medicines: {', '.join(all_meds)}
- Dosage: {dosage if dosage else 'Not specified'}
- Duration: {duration_taken}

**Post-Medication Experience:**
{experience}

**Self-Reported Severity:** {severity}

Please provide a structured educational response:
1. **Understanding Your Experience** - Briefly explain what the described experience might relate to (educational, not diagnostic)
2. **Possible Contributing Factors** - List 2-3 factors that could be contributing to this experience
3. **Key Precaution to Watch For** - ONE clear, important precaution or sign to watch for
4. **General Suggestions** - 2-3 simple comfort measures or adjustments
5. **When to Seek Help** - Clear indicators of when to contact a healthcare provider

Keep the tone warm, reassuring, educational, and non-diagnostic. Use simple language.
Keep response under 250 words.
End with: "⚕️ This analysis is educational only. Always consult your doctor about medication side effects."
"""
                result = generate_ai_summary(prompt, api_key)
                if result["success"]:
                    st.markdown(f"""
                    <div class="ai-response-card">
                        <div class="ai-header">🤖 Educational Insight</div>
                        <div class="ai-content">{result['response']}</div>
                    </div>
                    """, unsafe_allow_html=True)

                    # Summary card
                    st.markdown("""
                    <div class="summary-card">
                        <h4>📌 Quick Reference</h4>
                        <ul>
                            <li>Your experience has been logged for your reference</li>
                            <li>Track any changes in your symptoms over the coming days</li>
                            <li>Share this information with your healthcare provider at your next visit</li>
                            <li>If symptoms worsen suddenly, seek medical attention promptly</li>
                        </ul>
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.error(f"AI analysis unavailable: {result['error']}")
        else:
            st.markdown("""
            <div class="warning-banner">
                <span class="warning-icon">🔑</span>
                <span>Enter your <strong>Gemini API key</strong> in the sidebar to receive AI-powered analysis 
                of your post-medication experience.</span>
            </div>
            """, unsafe_allow_html=True)

            # Still show a basic summary
            st.markdown("### 📊 Experience Logged")
            st.markdown(f"""
            <div class="summary-card">
                <p><strong>Medicines:</strong> {', '.join(all_meds)}</p>
                <p><strong>Severity:</strong> {severity}</p>
                <p><strong>Duration on medication:</strong> {duration_taken}</p>
                <p><strong>Experience:</strong> {experience[:200]}{'...' if len(experience) > 200 else ''}</p>
                <br>
                <p>💡 <em>To receive AI-powered educational insights, please add your Gemini API key.</em></p>
            </div>
            """, unsafe_allow_html=True)

    # Disclaimer
    st.markdown("---")
    st.markdown("""
    <div class="disclaimer">
        ⚕️ <strong>Disclaimer:</strong> This tool provides educational insights only, not medical diagnosis. 
        If you are experiencing unexpected or severe side effects, contact your healthcare provider immediately. 
        Never stop or change medication without consulting your doctor.
    </div>
    """, unsafe_allow_html=True)

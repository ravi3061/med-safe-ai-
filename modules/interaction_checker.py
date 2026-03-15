"""
Medicine Interaction Checker module.
Allows users to select medicines and check for known drug-drug interactions.
"""
import streamlit as st
from utils.fuzzy_match import get_all_medicine_names, check_interactions, get_medicine_info
from utils.ocr_helper import generate_ai_summary


def render():
    """Render the Medicine Interaction Checker page."""
    st.markdown("""
    <div class="page-header">
        <h1>💊 Medicine Interaction Checker</h1>
        <p class="subtitle">Check potential drug-drug interactions between your medicines</p>
    </div>
    """, unsafe_allow_html=True)

    # Info banner
    st.markdown("""
    <div class="info-banner">
        <span class="info-icon">ℹ️</span>
        <span>Select two or more medicines below to check for known interactions. 
        Medicine names are matched using intelligent fuzzy matching for accuracy.</span>
    </div>
    """, unsafe_allow_html=True)

    all_medicines = get_all_medicine_names()

    # Medicine selection
    col1, col2 = st.columns([3, 1])
    with col1:
        selected_medicines = st.multiselect(
            "Select Medicines",
            options=all_medicines,
            placeholder="Start typing to search medicines...",
            help="Select at least 2 medicines to check interactions",
        )

    with col2:
        st.markdown("<br>", unsafe_allow_html=True)
        manual_entry = st.text_input(
            "Or type a name",
            placeholder="e.g. Paracetamol",
            help="Type a medicine name for fuzzy lookup",
        )

    # Handle manual entry with fuzzy matching
    if manual_entry:
        from utils.fuzzy_match import fuzzy_match_medicine
        matches = fuzzy_match_medicine(manual_entry, threshold=60, limit=3)
        if matches:
            st.markdown("**🔍 Fuzzy matches found:**")
            for m in matches:
                confidence_color = "#10b981" if m["score"] >= 85 else "#f59e0b" if m["score"] >= 70 else "#ef4444"
                st.markdown(f"""
                <div class="match-card">
                    <span class="match-name">{m['name']}</span>
                    <span class="match-salt">({m['active_salt']})</span>
                    <span class="match-score" style="color: {confidence_color}">
                        {m['score']}% match
                    </span>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.warning("No matches found. Try a different spelling.")

    # Display selected medicine details
    if selected_medicines:
        st.markdown("### 📋 Selected Medicines")
        cols = st.columns(min(len(selected_medicines), 3))
        for idx, med_name in enumerate(selected_medicines):
            with cols[idx % 3]:
                info = get_medicine_info(med_name)
                if info:
                    st.markdown(f"""
                    <div class="med-card">
                        <div class="med-name">{info['name']}</div>
                        <div class="med-salt">🧬 {info['active_salt']}</div>
                        <div class="med-category">📂 {info['category']}</div>
                        <div class="med-use">💡 {info['common_use']}</div>
                    </div>
                    """, unsafe_allow_html=True)

    # Check interactions
    if len(selected_medicines) >= 2:
        st.markdown("---")
        if st.button("🔬 Check Interactions", use_container_width=True, type="primary"):
            with st.spinner("Analyzing drug interactions..."):
                interactions = check_interactions(selected_medicines)

            if interactions:
                st.markdown(f"### ⚠️ {len(interactions)} Interaction(s) Found")

                for interaction in interactions:
                    severity = interaction["severity"]
                    if severity == "severe":
                        severity_color = "#ef4444"
                        severity_bg = "rgba(239, 68, 68, 0.1)"
                        severity_icon = "🔴"
                    elif severity == "moderate":
                        severity_color = "#f59e0b"
                        severity_bg = "rgba(245, 158, 11, 0.1)"
                        severity_icon = "🟡"
                    else:
                        severity_color = "#10b981"
                        severity_bg = "rgba(16, 185, 129, 0.1)"
                        severity_icon = "🟢"

                    st.markdown(f"""
                    <div class="interaction-card" style="border-left: 4px solid {severity_color}; background: {severity_bg};">
                        <div class="interaction-header">
                            <span class="interaction-drugs">{interaction['drug_a']} ↔ {interaction['drug_b']}</span>
                            <span class="severity-badge" style="background: {severity_color};">
                                {severity_icon} {severity.upper()}
                            </span>
                        </div>
                        <div class="interaction-desc">{interaction['description']}</div>
                    </div>
                    """, unsafe_allow_html=True)

                # AI Safety Note
                api_key = st.session_state.get("gemini_api_key", "")
                if api_key:
                    st.markdown("### 🤖 AI Safety Summary")
                    with st.spinner("Generating AI safety note..."):
                        interaction_text = "\n".join(
                            [f"- {i['drug_a']} + {i['drug_b']} ({i['severity']}): {i['description']}"
                             for i in interactions]
                        )
                        prompt = f"""You are a medication safety educator. Based on these drug interactions, 
provide a brief, clear safety summary in simple language. Be educational, not diagnostic.
Include: (1) What the user should be aware of, (2) General precautions, (3) When to consult a doctor.
Keep it under 150 words. Do not provide medical advice or diagnosis.

Medicines: {', '.join(selected_medicines)}
Interactions found:
{interaction_text}

End with: "⚕️ Always consult your doctor or pharmacist before combining medications."
"""
                        result = generate_ai_summary(prompt, api_key)
                        if result["success"]:
                            st.markdown(f"""
                            <div class="ai-response-card">
                                <div class="ai-header">🤖 AI Safety Note</div>
                                <div class="ai-content">{result['response']}</div>
                            </div>
                            """, unsafe_allow_html=True)
                        else:
                            st.error(f"AI summary unavailable: {result['error']}")
                else:
                    st.info("💡 Enter your Gemini API key in the sidebar to get AI-powered safety summaries.")
            else:
                st.markdown("""
                <div class="success-card">
                    <div class="success-icon">✅</div>
                    <div class="success-text">
                        <strong>No Known Interactions Found</strong><br>
                        No interactions were found between the selected medicines in our database. 
                        However, always confirm with your doctor or pharmacist.
                    </div>
                </div>
                """, unsafe_allow_html=True)
    elif selected_medicines:
        st.info("📌 Select at least **2 medicines** to check for interactions.")

    # Disclaimer
    st.markdown("---")
    st.markdown("""
    <div class="disclaimer">
        ⚕️ <strong>Disclaimer:</strong> This tool checks against a curated educational database only. 
        It does not cover all possible interactions. Always consult a qualified healthcare professional 
        before making any medication decisions.
    </div>
    """, unsafe_allow_html=True)

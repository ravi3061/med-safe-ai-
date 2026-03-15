"""
Prescription Image Analyzer module.
Uses Gemini Vision to extract medicine names and active salts from prescription images.
"""
import streamlit as st
import pandas as pd
from utils.ocr_helper import extract_medicines_from_image
from utils.fuzzy_match import get_best_match, check_interactions


def render():
    """Render the Prescription Image Analyzer page."""
    st.markdown("""
    <div class="page-header">
        <h1>📄 Prescription Analyzer</h1>
        <p class="subtitle">Upload a prescription image to extract medicines and active ingredients</p>
    </div>
    """, unsafe_allow_html=True)

    api_key = st.session_state.get("gemini_api_key", "")

    if not api_key:
        st.markdown("""
        <div class="warning-banner">
            <span class="warning-icon">🔑</span>
            <span>Please enter your <strong>Google Gemini API key</strong> in the sidebar to use this feature.
            The API key is required for AI-powered prescription analysis.</span>
        </div>
        """, unsafe_allow_html=True)
        return

    # Upload section
    st.markdown("""
    <div class="info-banner">
        <span class="info-icon">📸</span>
        <span>Upload a clear image of your prescription. Supported formats: JPG, JPEG, PNG. 
        The AI will extract medicine names, dosages, and active salts.</span>
    </div>
    """, unsafe_allow_html=True)

    uploaded_file = st.file_uploader(
        "Upload Prescription Image",
        type=["jpg", "jpeg", "png"],
        help="Upload a clear, well-lit photo of your prescription",
    )

    if uploaded_file is not None:
        col1, col2 = st.columns([1, 1])

        with col1:
            st.markdown("### 📷 Uploaded Prescription")
            st.image(uploaded_file, use_container_width=True)

        with col2:
            st.markdown("### 📊 Analysis Results")

            if st.button("🔍 Analyze Prescription", use_container_width=True, type="primary"):
                with st.spinner("🤖 AI is analyzing your prescription..."):
                    result = extract_medicines_from_image(uploaded_file, api_key)

                st.session_state["prescription_result"] = result

        # Display results
        if "prescription_result" in st.session_state:
            result = st.session_state["prescription_result"]

            if result["success"] and result["medicines"]:
                medicines = result["medicines"]

                st.markdown("---")
                st.markdown(f"### 💊 {len(medicines)} Medicine(s) Extracted")

                # Display as styled cards
                for idx, med in enumerate(medicines):
                    med_name = med.get("medicine_name", "Unknown")
                    active_salt = med.get("active_salt", "N/A")
                    dosage = med.get("dosage", "N/A")
                    frequency = med.get("frequency", "N/A")
                    duration = med.get("duration", "N/A")

                    st.markdown(f"""
                    <div class="prescription-card">
                        <div class="rx-number">Rx {idx + 1}</div>
                        <div class="rx-name">{med_name}</div>
                        <div class="rx-details">
                            <span class="rx-detail">🧬 Salt: <strong>{active_salt}</strong></span>
                            <span class="rx-detail">💉 Dosage: <strong>{dosage}</strong></span>
                            <span class="rx-detail">🔄 Frequency: <strong>{frequency}</strong></span>
                            <span class="rx-detail">📅 Duration: <strong>{duration}</strong></span>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)

                # Display as table too
                st.markdown("### 📋 Summary Table")
                df = pd.DataFrame(medicines)
                st.dataframe(df, use_container_width=True, hide_index=True)

                # Additional prescription info
                if result.get("doctor_name") and result["doctor_name"] != "N/A":
                    st.markdown(f"**👨‍⚕️ Doctor:** {result['doctor_name']}")
                if result.get("patient_name") and result["patient_name"] != "N/A":
                    st.markdown(f"**🧑 Patient:** {result['patient_name']}")
                if result.get("date") and result["date"] != "N/A":
                    st.markdown(f"**📅 Date:** {result['date']}")
                if result.get("notes"):
                    st.markdown(f"**📝 Notes:** {result['notes']}")

                # Cross-check option
                st.markdown("---")
                st.markdown("### 🔬 Cross-Check Interactions")
                st.markdown("Check if the extracted medicines have any known interactions:")

                extracted_names = [m.get("medicine_name", "") for m in medicines]
                # Try fuzzy matching against our database
                matched_names = []
                for name in extracted_names:
                    match = get_best_match(name, threshold=65)
                    if match:
                        matched_names.append(match["name"])

                if len(matched_names) >= 2:
                    if st.button("🔬 Check Extracted Medicine Interactions", use_container_width=True):
                        interactions = check_interactions(matched_names)
                        if interactions:
                            st.warning(f"⚠️ {len(interactions)} interaction(s) found!")
                            for i in interactions:
                                severity = i["severity"]
                                icon = "🔴" if severity == "severe" else "🟡" if severity == "moderate" else "🟢"
                                st.markdown(f"""
                                <div class="interaction-card" style="border-left: 4px solid {'#ef4444' if severity == 'severe' else '#f59e0b' if severity == 'moderate' else '#10b981'};">
                                    <div class="interaction-header">
                                        <span>{icon} <strong>{i['drug_a']} ↔ {i['drug_b']}</strong> — {severity.upper()}</span>
                                    </div>
                                    <div class="interaction-desc">{i['description']}</div>
                                </div>
                                """, unsafe_allow_html=True)
                        else:
                            st.success("✅ No known interactions found between the extracted medicines.")
                elif matched_names:
                    st.info("Only one medicine could be matched in our database. Add more medicines to check interactions.")
                else:
                    st.info("Could not match extracted medicine names with our database for interaction checking.")

            elif result.get("error"):
                st.error(f"❌ {result['error']}")
                if result.get("raw_response"):
                    with st.expander("🔧 Raw AI Response"):
                        st.code(result["raw_response"])
            else:
                st.warning("No medicines could be extracted. Please try with a clearer image.")

    # Disclaimer
    st.markdown("---")
    st.markdown("""
    <div class="disclaimer">
        ⚕️ <strong>Disclaimer:</strong> AI-based prescription reading is for educational purposes only. 
        OCR and AI analysis may contain errors. Always verify with your pharmacist or doctor. 
        Never rely solely on this tool for medication decisions.
    </div>
    """, unsafe_allow_html=True)

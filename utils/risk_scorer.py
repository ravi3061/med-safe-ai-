"""
Rule-based emergency risk scoring module.
Assigns a 0-100 risk score based on symptoms, age, and severity indicators.
"""

# Symptom risk weights
SYMPTOM_RISK_MAP = {
    "chest pain": 25,
    "chest tightness": 22,
    "shortness of breath": 22,
    "difficulty breathing": 25,
    "severe headache": 15,
    "sudden vision loss": 20,
    "blurred vision": 10,
    "fainting": 20,
    "loss of consciousness": 25,
    "seizure": 25,
    "numbness on one side": 22,
    "slurred speech": 25,
    "difficulty speaking": 22,
    "rapid heartbeat": 15,
    "palpitations": 12,
    "severe allergic reaction": 22,
    "throat swelling": 25,
    "difficulty swallowing": 15,
    "high fever": 15,
    "fever above 103": 18,
    "blood in vomit": 20,
    "blood in stool": 18,
    "blood in urine": 15,
    "coughing blood": 20,
    "severe abdominal pain": 18,
    "persistent vomiting": 14,
    "severe dehydration": 18,
    "confusion": 20,
    "disorientation": 18,
    "blue lips": 25,
    "blue fingertips": 22,
    "swelling in legs": 12,
    "severe dizziness": 15,
    "uncontrolled bleeding": 22,
    "suicidal thoughts": 30,
    "self harm": 30,
    "sudden weakness": 18,
    "inability to move": 20,
    "severe burn": 18,
    "head injury": 20,
    "eye injury": 15,
    "poisoning": 25,
    "overdose": 30,
    "snake bite": 25,
    "drowning": 30,
    "electric shock": 22,
}

# Critical symptom combinations that elevate risk
CRITICAL_COMBINATIONS = [
    ({"chest pain", "shortness of breath"}, 15),
    ({"chest pain", "numbness on one side"}, 20),
    ({"slurred speech", "numbness on one side"}, 25),
    ({"high fever", "confusion"}, 15),
    ({"severe headache", "confusion"}, 15),
    ({"difficulty breathing", "blue lips"}, 20),
    ({"fainting", "chest pain"}, 18),
    ({"seizure", "high fever"}, 15),
    ({"blood in vomit", "severe abdominal pain"}, 15),
    ({"rapid heartbeat", "chest pain"}, 15),
    ({"throat swelling", "difficulty breathing"}, 20),
]

# Urgency levels based on score
URGENCY_LEVELS = {
    (0, 20): {
        "level": "Low",
        "color": "green",
        "emoji": "🟢",
        "label": "Monitor at Home",
        "guidance": "Your symptoms appear to be low-risk. Continue to monitor and practice self-care. "
                    "Consult a doctor if symptoms persist or worsen over the next 24-48 hours.",
    },
    (20, 40): {
        "level": "Moderate",
        "color": "gold",
        "emoji": "🟡",
        "label": "Schedule a Doctor Visit",
        "guidance": "Your symptoms suggest moderate concern. Schedule an appointment with your doctor "
                    "within the next 1-2 days. Monitor symptoms closely and seek immediate help if they worsen.",
    },
    (40, 65): {
        "level": "High",
        "color": "orange",
        "emoji": "🟠",
        "label": "Seek Medical Attention Soon",
        "guidance": "Your symptom profile indicates elevated risk. Please visit a healthcare provider today "
                    "or go to an urgent care center. Do not delay if symptoms intensify.",
    },
    (65, 101): {
        "level": "Critical",
        "color": "red",
        "emoji": "🔴",
        "label": "Emergency — Seek Immediate Help",
        "guidance": "Your symptoms indicate a potentially serious situation. Please call emergency services "
                    "or go to the nearest emergency room immediately. Do not wait.",
    },
}


def calculate_risk_score(symptoms, age=None, gender=None):
    """
    Calculate a risk score (0-100) based on reported symptoms.

    Args:
        symptoms: List of symptom strings (lowercase).
        age: Optional patient age (int).
        gender: Optional patient gender string.

    Returns:
        dict with keys: score, urgency_level, urgency_color, urgency_emoji,
                        urgency_label, guidance, matched_symptoms, risk_factors
    """
    if not symptoms:
        return {
            "score": 0,
            "urgency_level": "Low",
            "urgency_color": "green",
            "urgency_emoji": "🟢",
            "urgency_label": "No Symptoms Reported",
            "guidance": "No symptoms were provided for assessment.",
            "matched_symptoms": [],
            "risk_factors": [],
        }

    symptoms_lower = [s.lower().strip() for s in symptoms]
    symptoms_set = set(symptoms_lower)

    # Base score from individual symptoms
    base_score = 0
    matched = []
    for symptom in symptoms_lower:
        for key, weight in SYMPTOM_RISK_MAP.items():
            if key in symptom or symptom in key:
                base_score += weight
                matched.append((symptom, weight))
                break

    # Bonus for critical combinations
    combo_bonus = 0
    risk_factors = []
    for combo_set, bonus in CRITICAL_COMBINATIONS:
        if combo_set.issubset(symptoms_set):
            combo_bonus += bonus
            risk_factors.append(f"Critical combination: {' + '.join(combo_set)}")

    # Age-based adjustment
    age_adjustment = 0
    if age is not None:
        if age < 5:
            age_adjustment = 8
            risk_factors.append("Age under 5 — higher vulnerability")
        elif age > 65:
            age_adjustment = 10
            risk_factors.append("Age over 65 — higher vulnerability")
        elif age > 50:
            age_adjustment = 5
            risk_factors.append("Age over 50 — moderate age factor")

    # Multiple symptom penalty
    count_adjustment = 0
    if len(matched) >= 4:
        count_adjustment = 8
        risk_factors.append("Multiple symptoms reported (4+)")
    elif len(matched) >= 3:
        count_adjustment = 4
        risk_factors.append("Multiple symptoms reported (3+)")

    # Final score (capped at 100)
    total = min(base_score + combo_bonus + age_adjustment + count_adjustment, 100)

    # Determine urgency level
    urgency = None
    for (low, high), info in URGENCY_LEVELS.items():
        if low <= total < high:
            urgency = info
            break

    if urgency is None:
        urgency = list(URGENCY_LEVELS.values())[-1]

    return {
        "score": total,
        "urgency_level": urgency["level"],
        "urgency_color": urgency["color"],
        "urgency_emoji": urgency["emoji"],
        "urgency_label": urgency["label"],
        "guidance": urgency["guidance"],
        "matched_symptoms": matched,
        "risk_factors": risk_factors,
    }


def get_available_symptoms():
    """Return a sorted list of all symptoms in the risk map."""
    return sorted(SYMPTOM_RISK_MAP.keys())

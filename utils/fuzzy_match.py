"""
Fuzzy matching utility for medicine name resolution.
Uses rapidfuzz to match user-entered names against the curated medicines database.
"""
import os
import pandas as pd
from rapidfuzz import fuzz, process

# Load medicines database
_DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")
_medicines_df = None


def _load_medicines():
    """Lazy-load the medicines database."""
    global _medicines_df
    if _medicines_df is None:
        _medicines_df = pd.read_csv(os.path.join(_DATA_DIR, "medicines.csv"))
    return _medicines_df


def get_all_medicine_names():
    """Return a sorted list of all medicine names in the database."""
    df = _load_medicines()
    return sorted(df["name"].unique().tolist())


def fuzzy_match_medicine(query, threshold=70, limit=5):
    """
    Match a user-entered medicine name against the database using fuzzy matching.

    Args:
        query: User-entered medicine name string.
        threshold: Minimum similarity score (0-100) to consider a match.
        limit: Maximum number of matches to return.

    Returns:
        List of dicts with keys: name, active_salt, category, common_use, score
    """
    df = _load_medicines()
    names = df["name"].tolist()

    results = process.extract(
        query,
        names,
        scorer=fuzz.WRatio,
        limit=limit,
        score_cutoff=threshold,
    )

    matches = []
    for name, score, idx in results:
        row = df[df["name"] == name].iloc[0]
        matches.append({
            "name": row["name"],
            "active_salt": row["active_salt"],
            "category": row["category"],
            "common_use": row["common_use"],
            "score": round(score, 1),
        })
    return matches


def get_best_match(query, threshold=70):
    """
    Return the single best fuzzy match for a query, or None if below threshold.
    """
    matches = fuzzy_match_medicine(query, threshold=threshold, limit=1)
    return matches[0] if matches else None


def get_medicine_info(name):
    """
    Get exact medicine info by name. Returns dict or None.
    """
    df = _load_medicines()
    row = df[df["name"].str.lower() == name.lower()]
    if row.empty:
        return None
    r = row.iloc[0]
    return {
        "name": r["name"],
        "active_salt": r["active_salt"],
        "category": r["category"],
        "common_use": r["common_use"],
    }


def check_interactions(medicine_names):
    """
    Check for known drug-drug interactions among a list of medicine names.

    Args:
        medicine_names: List of medicine name strings.

    Returns:
        List of dicts with keys: drug_a, drug_b, severity, description
    """
    interactions_df = pd.read_csv(os.path.join(_DATA_DIR, "interactions.csv"))
    found = []
    names_lower = [n.lower() for n in medicine_names]

    for _, row in interactions_df.iterrows():
        a_lower = row["drug_a"].lower()
        b_lower = row["drug_b"].lower()
        if a_lower in names_lower and b_lower in names_lower:
            found.append({
                "drug_a": row["drug_a"],
                "drug_b": row["drug_b"],
                "severity": row["severity"],
                "description": row["description"],
            })

    return found

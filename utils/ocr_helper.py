"""
OCR and prescription parsing helper using Google Gemini Vision.
Sends prescription images to Gemini for medicine and salt extraction.
"""
import json
from google import genai
from PIL import Image


def extract_medicines_from_image(image_file, api_key):
    """
    Extract medicine names and active salts from a prescription image using Gemini Vision.

    Args:
        image_file: Uploaded file object (from st.file_uploader) or file path string.
        api_key: Google Gemini API key.

    Returns:
        dict with keys: success, medicines (list of dicts), raw_response, error
    """
    try:
        client = genai.Client(api_key=api_key)

        # Load image
        if isinstance(image_file, str):
            img = Image.open(image_file)
        else:
            img = Image.open(image_file)

        prompt = """Analyze this medical prescription image carefully.
Extract ALL medicine names mentioned in the prescription.

For each medicine found, provide:
1. medicine_name: The name of the medicine as written
2. active_salt: The active pharmaceutical ingredient / salt (if you can identify it)
3. dosage: The dosage mentioned (if visible)
4. frequency: How often to take it (if visible)
5. duration: For how long (if visible)

Return your response as a valid JSON object with this exact structure:
{
    "medicines": [
        {
            "medicine_name": "...",
            "active_salt": "...",
            "dosage": "...",
            "frequency": "...",
            "duration": "..."
        }
    ],
    "doctor_name": "..." (if visible),
    "patient_name": "..." (if visible),
    "date": "..." (if visible),
    "notes": "any additional observations"
}

If you cannot read certain parts clearly, indicate with "unclear" rather than guessing.
If this is not a prescription image, return: {"error": "This does not appear to be a medical prescription."}
Return ONLY the JSON, no additional text."""

        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=[prompt, img],
        )
        response_text = response.text.strip()

        # Clean up response - remove markdown code blocks if present
        if response_text.startswith("```"):
            lines = response_text.split("\n")
            response_text = "\n".join(lines[1:-1])

        parsed = json.loads(response_text)

        if "error" in parsed:
            return {
                "success": False,
                "medicines": [],
                "raw_response": response_text,
                "error": parsed["error"],
            }

        return {
            "success": True,
            "medicines": parsed.get("medicines", []),
            "raw_response": response_text,
            "error": None,
            "doctor_name": parsed.get("doctor_name", "N/A"),
            "patient_name": parsed.get("patient_name", "N/A"),
            "date": parsed.get("date", "N/A"),
            "notes": parsed.get("notes", ""),
        }

    except json.JSONDecodeError:
        return {
            "success": True,
            "medicines": [],
            "raw_response": response_text if 'response_text' in locals() else "",
            "error": "Could not parse structured data. See raw response.",
        }
    except Exception as e:
        return {
            "success": False,
            "medicines": [],
            "raw_response": "",
            "error": str(e),
        }


def generate_ai_summary(prompt_text, api_key, model_name="gemini-2.0-flash"):
    """
    Generate an AI response using Google Gemini.

    Args:
        prompt_text: The prompt to send to the model.
        api_key: Google Gemini API key.
        model_name: Gemini model to use.

    Returns:
        dict with keys: success, response, error
    """
    try:
        client = genai.Client(api_key=api_key)
        response = client.models.generate_content(
            model=model_name,
            contents=prompt_text,
        )
        return {
            "success": True,
            "response": response.text,
            "error": None,
        }
    except Exception as e:
        return {
            "success": False,
            "response": "",
            "error": str(e),
        }

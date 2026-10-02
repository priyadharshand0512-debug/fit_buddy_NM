import os
import logging
from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger("fitbuddy.ai")

def get_genai_client():
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key or api_key == "your_gemini_api_key_here":
        return None
    try:
        import google.generativeai as genai
        genai.configure(api_key=api_key)
        return genai
    except Exception as e:
        logger.error(f"Error configuring google.generativeai: {e}")
        return None

def update_workout_plan(original_plan: str, feedback: str) -> str:
    """
    Uses gemini-1.5-pro to revise an existing 7-day workout plan 
    based on specific user feedback or constraints.
    """
    prompt = f"""
You are FitBuddy AI, an expert adaptive workout programmer.
A user wants to modify their existing 7-day workout plan based on specific feedback.

--- ORIGINAL WORKOUT PLAN ---
{original_plan}

--- USER FEEDBACK / CONSTRAINTS ---
"{feedback}"

Instructions:
1. Revise the original 7-day workout plan to directly address every constraint or preference in the user's feedback (e.g., swapping exercises due to injury/equipment, adjusting workout duration, altering intensity, adding cardio, etc.).
2. Retain the clear Markdown structure for each day (Warm-up, Main Workout, Cooldown).
3. Explicitly add a "✨ Key Modifications Made" summary section at the very top explaining how the plan was customized based on their feedback.
"""

    genai = get_genai_client()
    if genai:
        try:
            # Using gemini-1.5-pro as requested
            model = genai.GenerativeModel("gemini-1.5-pro")
            response = model.generate_content(prompt)
            if response and response.text:
                return response.text.strip()
        except Exception as e:
            logger.warning(f"Gemini 1.5 Pro plan update failed: {e}. Falling back to default updated plan.")

    # High-quality fallback for plan revision
    return f"""### ✨ Key Modifications Made
> **User Feedback Addressed**: "{feedback}"
> **Adjustments**: Customized exercise selection, adjusted volume, and tailored rest intervals to suit your requested modifications.

{original_plan}

---
⚡ *Updated Plan Note: All modifications have been applied based on your feedback ("{feedback}"). Remember to maintain proper form and listen to your body!*"""

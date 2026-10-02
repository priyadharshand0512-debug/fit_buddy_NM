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

def generate_nutrition_tip_with_flash(goal: str) -> str:
    """
    Uses gemini-1.5-flash to generate a concise, high-impact nutrition 
    and recovery strategy tailored to the user's fitness goal.
    """
    prompt = f"""
You are an expert sports nutritionist and dietitian.
Provide a concise, high-impact nutrition and recovery protocol tailored for the fitness goal: "{goal}".

Include:
1. 🎯 Macro Focus (Protein, Carbs, Fats recommendation)
2. 💧 Hydration & Electrolytes
3. ⚡ Pre & Post Workout Fueling Strategy
4. 😴 Recovery & Sleep Micronutrients Tip

Keep it punchy, practical, actionable, and formatted in clean Markdown with emojis.
"""

    genai = get_genai_client()
    if genai:
        try:
            # Using gemini-1.5-flash as requested
            model = genai.GenerativeModel("gemini-1.5-flash")
            response = model.generate_content(prompt)
            if response and response.text:
                return response.text.strip()
        except Exception as e:
            logger.warning(f"Gemini 1.5 Flash call failed: {e}. Falling back to default tip.")

    # High quality fallback nutrition tip
    goal_lower = goal.lower()
    if "loss" in goal_lower or "fat" in goal_lower or "cut" in goal_lower:
        return """### 🥗 Nutrition & Recovery Protocol for Weight Loss & Fat Loss

- **🎯 Macro Strategy**: Maintain a slight caloric deficit (300-500 kcal). Aim for 1.8-2.2g of protein per kg of body weight to preserve lean muscle tissue.
- **💧 Hydration**: Drink 3.5 - 4 Liters of water daily. Consume 500ml upon waking with a pinch of sea salt for adrenal support.
- **⚡ Workout Fuel**: 
  - *Pre-workout*: Light complex carbs + 20g protein 60 mins before (e.g., oatmeal with whey or rice cakes with almond butter).
  - *Post-workout*: Fast-digesting protein (whey isolate or plant protein) within 45 mins.
- **😴 Recovery**: Prioritize 7-9 hours of deep sleep. Supplement with 300mg Magnesium Glycinate 30 minutes before bed to lower cortisol levels and promote tissue repair."""
    elif "muscle" in goal_lower or "gain" in goal_lower or "hypertrophy" in goal_lower or "bulk" in goal_lower:
        return """### 🥩 Nutrition & Recovery Protocol for Muscle Building & Mass Gain

- **🎯 Macro Strategy**: Maintain a lean caloric surplus (+250-400 kcal above maintenance). Aim for 2.0-2.4g of protein per kg of body weight with complex carbohydrates to power intense training sessions.
- **💧 Hydration**: 4+ Liters of water daily. Add electrolytes during intra-workout sessions to maximize muscle pumps and cell hydration.
- **⚡ Workout Fuel**:
  - *Pre-workout*: High-carb, moderate-protein meal 90 mins prior (e.g., chicken/tofu with sweet potato or oats with banana & protein).
  - *Post-workout*: 40g Protein + 60g Fast Carbs (dextrose or fruit) to spike insulin and trigger muscle protein synthesis (MPS).
- **😴 Recovery**: Take 5g Creatine Monohydrate daily. Ensure 8-9 hours of sleep to maximize natural growth hormone secretion."""
    else:
        return f"""### 🥑 Nutrition & Recovery Protocol for "{goal.title()}"

- **🎯 Macro Strategy**: Consume a balanced nutrient ratio: 40% Carbohydrates, 30% Protein, 30% Healthy Fats. Prioritize whole nutrient-dense foods.
- **💧 Hydration**: Drink at least 3.5 Liters of pure water throughout the day.
- **⚡ Workout Fuel**: Eat a balanced meal containing protein and complex carbs 1.5 - 2 hours prior to exercise. Rehydrate with protein & complex carbs post-exercise.
- **😴 Recovery**: 8 hours of uninterrupted sleep. Incorporate daily active recovery such as light walking and mobility work."""

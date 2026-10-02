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

def generate_workout_gemini(goal: str, intensity: str) -> str:
    """
    Uses gemini-1.5-pro to generate a structured 7-day workout plan
    with warm-up, main workout, and cooldown for each day.
    """
    prompt = f"""
You are FitBuddy AI, an elite certified fitness trainer and strength coach.
Create a comprehensive, highly detailed 7-day workout plan tailored specifically for:
- Fitness Goal: {goal}
- Intensity Level: {intensity}

Required Formatting & Structure:
For EACH day (Day 1 through Day 7), format clearly with Markdown like this:

### 🏋️ Day X: [Focus / Title]
- **🔥 Warm-up (5-10 mins)**: 3-4 dynamic mobility exercises with reps/duration.
- **⚡ Main Workout (30-45 mins)**: 4-6 exercises with exact Sets, Reps, and Target RPE/Rest intervals.
- **🧘 Cooldown & Stretching (5-10 mins)**: 3 static stretches focusing on target muscles.

Provide actionable coaching notes, form cues, and progression recommendations at the end.
Make the formatting sleek, encouraging, and clean.
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
            logger.warning(f"Gemini 1.5 Pro call failed: {e}. Falling back to default plan.")

    # High quality fallback workout plan if API key is not present or API call fails
    return f"""### 🏋️ Day 1: Upper Body Strength & Power ({intensity.title()})
- **🔥 Warm-up (5-10 mins)**: 10 Arm Circles, 10 Band Pull-aparts, 10 Cat-Cows, 2 mins Light Joging/Jumping Jacks.
- **⚡ Main Workout (35 mins)**:
  1. Dumbbell/Barbell Bench Press: 4 Sets x 8-10 Reps (Rest: 90s)
  2. Bent-over Rows: 4 Sets x 10 Reps (Rest: 90s)
  3. Overhead Shoulder Press: 3 Sets x 12 Reps (Rest: 60s)
  4. Lat Pulldowns or Pull-ups: 3 Sets x 10-12 Reps (Rest: 60s)
  5. Bicep Curls superset with Tricep Dips: 3 Sets x 12 Reps (Rest: 45s)
- **🧘 Cooldown & Stretching (5 mins)**: Doorway Chest Stretch (45s), Overhead Tricep Stretch (45s), Upper Back Stretch (45s).

### 🏋️ Day 2: Lower Body & Core Focus
- **🔥 Warm-up (5-10 mins)**: Bodyweight Squats x 15, Leg Swings x 10/side, Glute Bridges x 15.
- **⚡ Main Workout (40 mins)**:
  1. Goblet Squats or Barbell Back Squats: 4 Sets x 8-10 Reps (Rest: 90s)
  2. Romanian Deadlifts (RDLs): 4 Sets x 10 Reps (Rest: 90s)
  3. Walking Lunges: 3 Sets x 12 Reps/leg (Rest: 60s)
  4. Calf Raises: 4 Sets x 15 Reps (Rest: 45s)
  5. Plank Holds: 3 Sets x 45-60 seconds (Rest: 45s)
- **🧘 Cooldown & Stretching (5 mins)**: Standing Quad Stretch (45s), Seated Hamstring Stretch (45s), Pigeon Pose (60s/side).

### 🏋️ Day 3: Active Recovery & Mobility
- **🔥 Warm-up (5 mins)**: World's Greatest Stretch x 5 per side, Light Walking.
- **⚡ Main Routine (30 mins)**:
  1. 20-30 minute Zone 2 Cardio (Brisk Walking, Swimming, or Cycling).
  2. Full-body Dynamic Yoga Flow / Mobility Routine.
- **🧘 Cooldown (5 mins)**: Deep Diaphragmatic Breathing and Foam Rolling (Quads, Calves, Thoracic Spine).

### 🏋️ Day 4: Push (Chest, Shoulders, Triceps)
- **🔥 Warm-up (5-10 mins)**: Push-up to Downward Dog x 8, Scapular Push-ups x 12, Shoulder Dislocates x 10.
- **⚡ Main Workout (35 mins)**:
  1. Incline Dumbbell Press: 4 Sets x 10 Reps (Rest: 75s)
  2. Dumbbell Lateral Raises: 4 Sets x 15 Reps (Rest: 45s)
  3. Bodyweight Dips or Machine Dips: 3 Sets x 10-12 Reps (Rest: 60s)
  4. Cable/Band Chest Flyes: 3 Sets x 12 Reps (Rest: 45s)
  5. Tricep Rope Pushdowns: 3 Sets x 15 Reps (Rest: 45s)
- **🧘 Cooldown & Stretching (5 mins)**: Cross-body Shoulder Stretch, Pec Stretch on Wall.

### 🏋️ Day 5: Pull (Back, Rear Delts, Biceps)
- **🔥 Warm-up (5-10 mins)**: Scapular Pull-ups x 10, Face Pulls with resistance band x 15.
- **⚡ Main Workout (40 mins)**:
  1. Conventional or Hex-bar Deadlifts / Romanian Deadlifts: 3 Sets x 6-8 Reps (Rest: 120s)
  2. Single-arm Dumbbell Rows: 4 Sets x 10 Reps/side (Rest: 60s)
  3. Face Pulls: 4 Sets x 15 Reps (Rest: 45s)
  4. Hammer Curls: 3 Sets x 12 Reps (Rest: 45s)
  5. Reverse Flyes: 3 Sets x 15 Reps (Rest: 45s)
- **🧘 Cooldown & Stretching (5 mins)**: Child's Pose (60s), Cobra Stretch (45s), Lat Stretch (45s/side).

### 🏋️ Day 6: Full Body High-Intensity & Endurance
- **🔥 Warm-up (5-10 mins)**: High Knees, Butt Kicks, Arm Swings, Torso Twists.
- **⚡ Main Workout (35 mins)**:
  1. Kettlebell Swings / Dumbbell Snatch: 4 Sets x 15 Reps
  2. Dumbbell Thrusters: 3 Sets x 12 Reps
  3. Mountain Climbers: 3 Sets x 45 Seconds
  4. Farmer's Carries: 3 Sets x 40 Meters
  5. Hanging Leg Raises or Hanging Knee Tucks: 3 Sets x 12 Reps
- **🧘 Cooldown & Stretching (5 mins)**: Full Body Stretch Flow and Controlled Hydration.

### 🏋️ Day 7: Complete Rest & Regeneration
- **⚡ Today's Focus**: Full Rest, Hydration, Muscle Tissue Repair.
- **🧘 Recommended**: Light 15-minute walk, contrast shower, 8+ hours of restful sleep, and foam rolling.

---
💡 *Coaching Tip for "{goal}" ({intensity}): Focus on progressive overload by increasing weight or reps by 2-5% each week while strictly maintaining proper exercise form!*"""

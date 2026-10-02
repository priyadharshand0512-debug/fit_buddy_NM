from fastapi import APIRouter, Request, Depends, Form, HTTPException, status
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
import os

from database import (
    get_db, 
    save_user, 
    save_plan, 
    update_plan, 
    get_original_plan, 
    get_user, 
    get_all_users, 
    get_all_plans
)
from ai_modules.gemini_generator import generate_workout_gemini
from ai_modules.gemini_flash_generator import generate_nutrition_tip_with_flash
from ai_modules.updated_plan import update_workout_plan

router = APIRouter()
templates = Jinja2Templates(directory="templates")

@router.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    """
    Renders the home page (index.html) with the user input form.
    """
    return templates.TemplateResponse("index.html", {"request": request})

@router.post("/generate-workout", response_class=HTMLResponse)
async def create_workout(
    request: Request,
    username: str = Form(...),
    user_id: str = Form(...),
    age: int = Form(...),
    weight: float = Form(...),
    goal: str = Form(...),
    intensity: str = Form(...),
    db: Session = Depends(get_db)
):
    """
    Captures form data, calls AI generators for workout plan & nutrition tip,
    saves user and plan to DB, and renders result.html.
    """
    user_id = user_id.strip()
    username = username.strip()

    if not user_id or not username:
        return templates.TemplateResponse(
            "index.html", 
            {
                "request": request, 
                "error": "Username and User ID are required fields."
            },
            status_code=status.HTTP_400_BAD_REQUEST
        )

    # Prepare user payload
    user_data = {
        "user_id": user_id,
        "username": username,
        "age": age,
        "weight": weight,
        "goal": goal,
        "intensity": intensity
    }

    # Save or update User in DB
    user_obj = save_user(db, user_data)

    # Generate AI Workout Plan & Nutrition Tip
    original_plan_text = generate_workout_gemini(goal=goal, intensity=intensity)
    nutrition_tip_text = generate_nutrition_tip_with_flash(goal=goal)

    # Save Plan in DB
    plan_obj = save_plan(
        db=db,
        user_id=user_id,
        original_plan=original_plan_text,
        nutrition_tip=nutrition_tip_text
    )

    return templates.TemplateResponse(
        "result.html",
        {
            "request": request,
            "user": user_obj,
            "original_plan": plan_obj.original_plan,
            "updated_plan": plan_obj.updated_plan,
            "nutrition_tip": plan_obj.nutrition_tip,
            "confirmation_message": None
        }
    )

@router.post("/submit-feedback", response_class=HTMLResponse)
async def submit_feedback(
    request: Request,
    user_id: str = Form(...),
    feedback: str = Form(...),
    db: Session = Depends(get_db)
):
    """
    Captures user_id and feedback, retrieves existing user & plan,
    calls update_workout_plan, saves updated plan to DB, and renders result.html.
    """
    user_id = user_id.strip()
    feedback = feedback.strip()

    if not user_id:
        return templates.TemplateResponse(
            "index.html",
            {"request": request, "error": "User ID is missing for feedback submission."},
            status_code=status.HTTP_400_BAD_REQUEST
        )

    user_obj = get_user(db, user_id)
    plan_obj = get_original_plan(db, user_id)

    if not user_obj or not plan_obj:
        return templates.TemplateResponse(
            "index.html",
            {"request": request, "error": f"No workout plan found for User ID: {user_id}. Please generate a plan first."},
            status_code=status.HTTP_404_NOT_FOUND
        )

    # Call AI to revise plan based on feedback
    revised_plan_text = update_workout_plan(
        original_plan=plan_obj.original_plan,
        feedback=feedback
    )

    # Save updated plan to DB
    updated_plan_obj = update_plan(db, user_id=user_id, new_updated_plan=revised_plan_text)

    return templates.TemplateResponse(
        "result.html",
        {
            "request": request,
            "user": user_obj,
            "original_plan": updated_plan_obj.original_plan,
            "updated_plan": updated_plan_obj.updated_plan,
            "nutrition_tip": updated_plan_obj.nutrition_tip,
            "confirmation_message": "🎉 Your workout plan has been successfully updated with your feedback!"
        }
    )

@router.get("/view-all-users", response_class=HTMLResponse)
async def view_all_users(
    request: Request,
    db: Session = Depends(get_db)
):
    """
    Admin Dashboard: Fetches all users and their respective workout plans.
    """
    users = get_all_users(db)
    plans = get_all_plans(db)

    # Map user_id to plan for easy template lookup
    user_plans_map = {plan.user_id: plan for plan in plans}

    users_data = []
    for u in users:
        plan = user_plans_map.get(u.user_id)
        users_data.append({
            "user": u,
            "plan": plan
        })

    return templates.TemplateResponse(
        "all_users.html",
        {
            "request": request,
            "users_data": users_data,
            "total_users": len(users_data)
        }
    )

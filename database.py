from typing import List, Optional
from datetime import datetime
from sqlalchemy import create_engine, Column, Integer, String, Float, Text, ForeignKey, DateTime
from sqlalchemy.orm import declarative_base, sessionmaker, Session, relationship

DATABASE_URL = "sqlite:///./fitbuddy.db"

engine = create_engine(
    DATABASE_URL, 
    connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String, unique=True, index=True, nullable=False)
    username = Column(String, nullable=False)
    age = Column(Integer, nullable=False)
    weight = Column(Float, nullable=False)
    goal = Column(String, nullable=False)
    intensity = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationship to Plan
    plans = relationship("Plan", back_populates="user", cascade="all, delete-orphan")

class Plan(Base):
    __tablename__ = "plans"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String, ForeignKey("users.user_id"), nullable=False)
    original_plan = Column(Text, nullable=False)
    updated_plan = Column(Text, nullable=True)
    nutrition_tip = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationship to User
    user = relationship("User", back_populates="plans")

def init_db():
    Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# CRUD Functions
def save_user(db: Session, user_data: dict) -> User:
    """
    Saves a new user or updates an existing user by user_id.
    user_data dict contains: user_id, username, age, weight, goal, intensity
    """
    existing_user = db.query(User).filter(User.user_id == user_data["user_id"]).first()
    if existing_user:
        existing_user.username = user_data["username"]
        existing_user.age = int(user_data["age"])
        existing_user.weight = float(user_data["weight"])
        existing_user.goal = user_data["goal"]
        existing_user.intensity = user_data["intensity"]
        db.commit()
        db.refresh(existing_user)
        return existing_user
    else:
        user = User(
            user_id=user_data["user_id"],
            username=user_data["username"],
            age=int(user_data["age"]),
            weight=float(user_data["weight"]),
            goal=user_data["goal"],
            intensity=user_data["intensity"]
        )
        db.add(user)
        db.commit()
        db.refresh(user)
        return user

def save_plan(db: Session, user_id: str, original_plan: str, updated_plan: Optional[str] = None, nutrition_tip: Optional[str] = None) -> Plan:
    """
    Saves a workout plan for a user.
    """
    existing_plan = db.query(Plan).filter(Plan.user_id == user_id).first()
    if existing_plan:
        existing_plan.original_plan = original_plan
        if updated_plan is not None:
            existing_plan.updated_plan = updated_plan
        if nutrition_tip is not None:
            existing_plan.nutrition_tip = nutrition_tip
        db.commit()
        db.refresh(existing_plan)
        return existing_plan
    else:
        plan = Plan(
            user_id=user_id,
            original_plan=original_plan,
            updated_plan=updated_plan,
            nutrition_tip=nutrition_tip
        )
        db.add(plan)
        db.commit()
        db.refresh(plan)
        return plan

def update_plan(db: Session, user_id: str, new_updated_plan: str) -> Optional[Plan]:
    """
    Updates the revised plan field for a user's plan.
    """
    plan = db.query(Plan).filter(Plan.user_id == user_id).first()
    if plan:
        plan.updated_plan = new_updated_plan
        db.commit()
        db.refresh(plan)
        return plan
    return None

def get_original_plan(db: Session, user_id: str) -> Optional[Plan]:
    """
    Retrieves the plan record for a given user_id.
    """
    return db.query(Plan).filter(Plan.user_id == user_id).first()

def get_user(db: Session, user_id: str) -> Optional[User]:
    """
    Retrieves a user by user_id.
    """
    return db.query(User).filter(User.user_id == user_id).first()

def get_all_users(db: Session) -> List[User]:
    """
    Fetches all registered users.
    """
    return db.query(User).order_by(User.id.desc()).all()

def get_all_plans(db: Session) -> List[Plan]:
    """
    Fetches all plans.
    """
    return db.query(Plan).all()

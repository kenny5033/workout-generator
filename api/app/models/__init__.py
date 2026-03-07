from enum import Enum
from pydantic import BaseModel
from sqlmodel import Relationship, SQLModel, Field, Session, select
from typing import Optional, List

from app.database import register_table_constructor


class WorkoutTypeChoice(str, Enum):
    PUSH = "push"
    PULL = "pull"
    CORE = "core"
    LEGS = "legs"


class WorkoutType(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: WorkoutTypeChoice = Field(unique=True, max_length=50)
    workouts: List["Workout"] = Relationship(back_populates="workout_type")


@register_table_constructor
def ConstructWorkoutTypes(session: Session):
    for workout_type in WorkoutTypeChoice:
        if not session.scalar(
            select(select(WorkoutType).where(WorkoutType.name == workout_type).exists())
        ):
            session.add(WorkoutType(name=workout_type))
    session.commit()


class Workout(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    workout_type_id: int = Field(foreign_key=f"{WorkoutType.__tablename__}.id")
    workout_type: WorkoutType = Relationship(back_populates="workouts")
    exercise: str = Field(unique=True, max_length=100)


class Routine(BaseModel):
    workouts: list[Workout]

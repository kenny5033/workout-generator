from typing import Sequence
from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError
from sqlmodel import Session, func, select
from starlette.status import HTTP_404_NOT_FOUND, HTTP_409_CONFLICT
from fastapi import APIRouter

from app.models import Routine, Workout, WorkoutType, WorkoutTypeChoice
from app.database import engine

router = APIRouter()


@router.get("/")
async def root() -> Routine:
    with Session(engine) as session:
        routine = Routine(workouts=[])
        for workout_type in WorkoutTypeChoice:
            workout = session.exec(
                select(Workout)
                .join(WorkoutType)
                .where(WorkoutType.name == workout_type)
                .order_by(func.random())
                .limit(1)
            ).first()

            if workout is not None:
                routine.workouts.append(workout)

        return routine


@router.get("/workout_types")
async def workout_types() -> Sequence[WorkoutType]:
    with Session(engine) as session:
        return session.exec(select(WorkoutType)).all()


@router.post("/add/")
async def add_workout(workout_type_id: int, name: str):
    with Session(engine) as session:
        workout_type = session.get(WorkoutType, workout_type_id)
        if workout_type is None:
            raise HTTPException(
                status_code=HTTP_404_NOT_FOUND, detail="Workout type does not exist"
            )

        session.add(Workout(workout_type=workout_type, exercise=name))

        try:
            session.commit()
        except IntegrityError:
            session.rollback()
            raise HTTPException(
                status_code=HTTP_409_CONFLICT, detail="Workout already exists"
            )

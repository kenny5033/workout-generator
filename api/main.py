from contextlib import asynccontextmanager
import random
from enum import Enum
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from starlette.status import HTTP_409_CONFLICT
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class WorkoutType(Enum):
    PUSH = "0"
    PULL = "1"
    CORE = "2"
    LEGS = "3"


class WorkoutTypeObject(BaseModel):
    id: str
    name: str


class Workout(BaseModel):
    type: WorkoutTypeObject
    exercise: str


class Routine(BaseModel):
    workouts: list[Workout]


class WorkoutManager:
    def __init__(self):
        self.loaded_workouts: dict[WorkoutType, list] = {}

        self._load_workouts()

    def _get_workouts_file_path(self, type: WorkoutType):
        return f"workouts/{type.name}"

    def _load_workouts(self):
        for workout_type in WorkoutType:
            with open(self._get_workouts_file_path(workout_type), "a+") as f:
                f.seek(0)
                self.loaded_workouts.setdefault(workout_type, [])
                for workout in f.readlines():
                    workout = workout.strip()
                    self.loaded_workouts[workout_type].append(workout)

    def reload(self):
        self._load_workouts

    def get_routine(self) -> Routine:
        routine = dict(workouts=[])
        for workout_type in WorkoutType:
            workouts = self.loaded_workouts[workout_type]
            workout = dict(
                type=WorkoutTypeObject.model_validate(
                    {"id": str(workout_type.value), "name": workout_type.name}
                ),
                exercise=random.choice(workouts) if workouts else "",
            )
            routine["workouts"].append(Workout.model_validate(workout))
        return Routine.model_validate(routine)

    def add_workout(self, type: WorkoutType, name: str):
        if name in self.loaded_workouts[type]:
            raise ValueError("This workout already exists")

        self.loaded_workouts[type].append(name)
        with open(self._get_workouts_file_path(type), "a") as f:
            f.write(name + "\n")

    def save(self):
        for workout_type in WorkoutType:
            with open(self._get_workouts_file_path(workout_type), "w") as f:
                f.writelines(
                    [workout + "\n" for workout in self.loaded_workouts[workout_type]]
                )


manager = WorkoutManager()


@asynccontextmanager
async def lifespan(app: FastAPI):
    # app startup
    yield
    # app shutdown
    manager.save()


app = FastAPI(lifespan=lifespan)


@app.get("/")
async def root() -> Routine:
    return manager.get_routine()


@app.post("/add/")
async def add_workout(workout_type_id: WorkoutType, name: str):
    workout_type = WorkoutType(workout_type_id)
    try:
        manager.add_workout(workout_type, name)
    except ValueError:
        raise HTTPException(
            status_code=HTTP_409_CONFLICT, detail="Workout already exists"
        )

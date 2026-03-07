export interface Workout {
  id?: number | null;
  workout_type_id: number;
  exercise: string;
}

export interface Routine {
  workouts: Workout[];
}

export interface ValidationError {
  loc: (string | number)[];
  msg: string;
  type: string;
  input?: unknown;
  ctx?: Record<string, unknown>;
}

export interface HTTPValidationError {
  detail?: ValidationError[];
}

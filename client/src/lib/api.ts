import type { Routine, HTTPValidationError } from './types';
import { PUBLIC_API_BASE_URL } from '$env/static/public';

export class ApiError extends Error {
	constructor(
		public status: number,
		public detail: HTTPValidationError | string
	) {
		super(`API error ${status}`);
	}
}

async function handleResponse<T>(res: Response): Promise<T> {
	if (!res.ok) {
		const detail = await res.json().catch(() => res.statusText);
		throw new ApiError(res.status, detail);
	}
	return res.json() as Promise<T>;
}

/** GET / — fetch the current routine */
export async function getRoutine(fetch: typeof globalThis.fetch): Promise<Routine> {
	const res = await fetch(`${PUBLIC_API_BASE_URL}/`);
	return handleResponse<Routine>(res);
}

/** POST /add/ — add a workout to the routine */
export async function addWorkout(
	fetch: typeof globalThis.fetch,
	params: { workout_type_id: number; name: string }
): Promise<unknown> {
	const url = new URL(`${PUBLIC_API_BASE_URL}/add/`);
	url.searchParams.set('workout_type_id', String(params.workout_type_id));
	url.searchParams.set('name', params.name);

	const res = await fetch(url.toString(), { method: 'POST' });
	return handleResponse<unknown>(res);
}

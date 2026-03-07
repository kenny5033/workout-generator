import type { PageLoad } from './$types';
import { getRoutine } from '$lib/api';

export const load: PageLoad = async ({ fetch }) => {
  const routine = await getRoutine(fetch);
  return { routine };
};

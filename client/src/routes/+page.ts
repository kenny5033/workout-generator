import type { PageLoad } from './$types';
import { PUBLIC_API_PROTOCOL, PUBLIC_API_HOSTNAME, PUBLIC_API_PORT } from '$env/static/public';

export const load: PageLoad = async ({ fetch }) => {
	const res = await fetch(`${PUBLIC_API_PROTOCOL}://${PUBLIC_API_HOSTNAME}:${PUBLIC_API_PORT}`);
	return await res.json();
};

import type { PageLoad } from "./$types";
import { DefaultApi } from "$lib/gen/openapi/apis/DefaultApi";
import { PUBLIC_API_BASE_URL } from "$env/static/public";
import { Configuration } from "$lib/gen/openapi";

const config = new Configuration({ basePath: PUBLIC_API_BASE_URL });
const api = new DefaultApi(config);

export const load: PageLoad = async () => {
  const routine = await api.rootGet();
  return { api, routine };
};

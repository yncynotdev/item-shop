import { useRuntimeConfig } from "#app";

export default defineNuxtRouteMiddleware(async (to, from) => {
  const config = useRuntimeConfig();

  const { data, error } = await authClient.token();
  if (error) return abortNavigation();
  if (!data.token) return abortNavigation();

  try {
    const token = data.token;

    await $fetch(`${config.public.fastApiUrl}${"/api/auth/verify"}`, {
      method: "GET",
      headers: {
        Authorization: `Bearer ${token}`,
      },
    });
  } catch (err) {
    return abortNavigation();
  }
});

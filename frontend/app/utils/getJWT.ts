import useJWT from "~/composables/useJWT";

export default async function getJWT() {
  const config = useRuntimeConfig();
  const jwt = useJWT();

  const { data, error } = await authClient.token();
  if (error || !data.token) return;

  jwt.value = data.token;

  await $fetch(`${config.public.fastApiUrl}${"/api/auth/verify"}`, {
    method: "GET",
    headers: {
      Authorization: `Bearer ${jwt.value}`,
    },
    credentials: "include",
  });

  return { jwt, error };
}

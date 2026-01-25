import getJWT from "~/utils/getJWT";

export default defineNuxtRouteMiddleware(async (to, from) => {
  const token = await getJWT();
  if (!token || !token.jwt.value) return abortNavigation();
});

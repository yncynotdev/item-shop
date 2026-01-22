import { createAuthClient } from "better-auth/vue";

export const authClient = createAuthClient({
  baseURL: process.env.BETTER_AUTH_URL,
});

export async function signInWithGitHub() {
  const data = await authClient.signIn.social({
    provider: "github",
  });

  return data;
}

export async function signInWithGoogle() {
  const data = await authClient.signIn.social({
    provider: "google",
  });

  return data;
}

export async function signOut() {
  await authClient.signOut();
}

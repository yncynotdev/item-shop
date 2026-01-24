import { createAuthClient } from "better-auth/vue";
import { jwtClient } from "better-auth/client/plugins";

export const authClient = createAuthClient({
  baseURL: process.env.BETTER_AUTH_URL,
  plugins: [jwtClient()],
});

export async function signInWithGitHub() {
  await authClient.signIn.social({
    provider: "github",
  });
}

export async function signInWithGoogle() {
  await authClient.signIn.social({
    provider: "google",
  });
}

export async function signOut() {
  await authClient.signOut();
}

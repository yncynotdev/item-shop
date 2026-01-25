<script setup lang="ts">
import * as z from "zod";
import type { FormSubmitEvent, AuthFormField } from "@nuxt/ui";

definePageMeta({
  layout: 'login'
})

const config = useRuntimeConfig()

const toast = useToast();

const session = authClient.useSession();

const isLoading = ref<boolean>(false);

const fields: AuthFormField[] = [
  {
    name: "email",
    type: "email",
    label: "Email",
    placeholder: "Enter your email",
    required: true,
  },
  {
    name: "password",
    type: "password",
    label: "Password",
    placeholder: "Enter your password",
    required: true,
  },
];

const providers = [
  {
    label: "Google",
    icon: "i-simple-icons-google",
    onClick: async() => {
      signInWithGoogle();
    },
  },
  {
    label: "GitHub",
    icon: "i-simple-icons-github",
    onClick: async() => {
      signInWithGitHub();
    },
  },
];

const schema = z.object({
  email: z.email("Invalid email"),
  password: z
    .string("Password is required")
    .min(8, "Must be at least 8 characters"),
});

type Schema = z.output<typeof schema>;

async function onSubmit(payload: FormSubmitEvent<Schema>) {
  await authClient.signIn.email(
    {
      email: payload.data.email,
      password: payload.data.password,
    },
    {
      onRequest: (_ctx) => {
        isLoading.value = true;
      },
      onSuccess: async (_ctx) => {
        await request()
      },
      onError: (ctx) => {
        toast.add({
          title: "Error",
          description: `${ctx.error.message}`,
          color: "error",
        });
      },
    },
  );
}

async function request() {
  const { data, error } = await authClient.token()
  if (error) throw error

  if (!data.token) {
    console.warn("No token found")
    return
  }

  if (data) {
    const token = data.token

    await $fetch(
      `${config.public.fastApiUrl}${"/api/auth/verify"}`,
      {
        method: "GET",
        headers: {
          Authorization: `Bearer ${token}`,
        },
      },
    );
  }
}
</script>

<template>
  <div class="flex flex-col items-center justify-center gap-4 p-4">
    <UPageCard class="w-full max-w-md">
      <UAuthForm 
        :schema="schema"
        title="Login"
        description="Enter your credentials to access your account."
        :fields="fields"
        :providers="providers"
        @submit="onSubmit"
      >
        <template #footer>
          <span>Don't have account?
            <NuxtLink to="/sign-up">Sign up here</NuxtLink>
          </span>
        </template>
      </UAuthForm>
    </UPageCard>

    <div>
      <UButton v-if="session.data" label="Logout" @click="signOut" />
    </div>
    <div>
      <UButton label="Request" @click="request" />
    </div>
    <div>
      <UButton label="Protected Route" to="/protected" />
    </div>
  </div>
</template>

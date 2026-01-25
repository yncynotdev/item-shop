<script setup lang="ts">
import * as z from "zod";
import type { FormSubmitEvent, AuthFormField } from "@nuxt/ui";

definePageMeta({
  layout: "login",
});

const toast = useToast();

const isLoading = ref<boolean>(false);

const fields: AuthFormField[] = [
  {
    name: "username",
    type: "text",
    label: "Username",
    placeholder: "Enter your username",
    required: true,
  },
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
    onClick: () => {
      signInWithGoogle();
    },
  },
  {
    label: "GitHub",
    icon: "i-simple-icons-github",
    onClick: () => {
      signInWithGitHub();
    },
  },
];

const schema = z.object({
  username: z.string("Username is required").max(50),
  email: z.email("Invalid email"),
  password: z
    .string("Password is required")
    .min(8, "Must be at least 8 characters"),
});

type Schema = z.output<typeof schema>;

async function onSubmit(payload: FormSubmitEvent<Schema>) {
  await authClient.signUp.email(
    {
      email: payload.data.email,
      password: payload.data.password,
      name: payload.data.username,
    },
    {
      onRequest: (_ctx) => {
        isLoading.value = true;
      },
      onSuccess: async (_ctx) => {
        toast.add({
          title: "Success",
          description: "User Created",
          color: "success",
        });

        await navigateTo("/");
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
</script>

<template>
  <div class="flex flex-col items-center justify-center gap-4 p-4">
    <UPageCard class="w-full max-w-md">
      <UAuthForm
        :schema="schema"
        title="Sign-In"
        description="Enter all the required fields to create account"
        :fields="fields" 
        :providers="providers"
        :submit="{
          loading: isLoading,
        }"
        @submit="onSubmit"
      >
        <template #footer>
          <div class="flex flex-col gap-5">
            <UButton 
              label="Go Back"
              color="neutral"
              variant="outline"
              to="/"
              class="flex flex-col justify-center"
            />
            <span>Have an account? <NuxtLink to="/login">Login here</NuxtLink></span>
          </div>
        </template>
      </UAuthForm>
    </UPageCard>
  </div>
</template>

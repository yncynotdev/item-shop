<script setup lang="ts">
import * as z from "zod";
import type { FormSubmitEvent, AuthFormField } from "@nuxt/ui";

const toast = useToast();

const session = authClient.useSession();

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
  email: z.email("Invalid email"),
  password: z
    .string("Password is required")
    .min(8, "Must be at least 8 characters"),
});

type Schema = z.output<typeof schema>;

function onSubmit(payload: FormSubmitEvent<Schema>) {
  toast.add({
    title: "Submitted",
    description: `${payload}`,
    color: "success",
  });
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
      />
    </UPageCard>
    <UButton v-if="session.data" label="Logout" @click="signOut" />
  </div>
</template>

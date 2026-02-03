<script setup lang="ts">
import * as z from "zod";
import type { FormSubmitEvent } from "@nuxt/ui";

const config = useRuntimeConfig();

const schema = z.object({
  name: z.string(),
  types: z.string(),
  quantity: z.number(),
  file: z.instanceof(File),
});

type Schema = z.output<typeof schema>;

const state = reactive<Partial<Schema>>({
  name: undefined,
  types: undefined,
  quantity: undefined,
  file: undefined,
});

const toast = useToast();
async function onSubmit(event: FormSubmitEvent<Schema>) {
  const form = new FormData();
  const file = event.data.file;


  form.append('name', event.data.name)
  form.append('types', event.data.types)
  form.append('quantity', String(event.data.quantity))
  form.append("file", file as File);

  try {
    await $fetch(`${config.public.fastApiUrl}/items/`, {
      method: "POST",
      body: form,
    });
    toast.add({
      title: "Succes",
      description: "Item has been added",
      color: "success",
    });
  } catch (error) {
    toast.add({
      title: "Error",
      description: "There's an error occured",
      color: "error",
    });
  }
}
</script>

<template>
  <UModal title="Add Items" description="Upload your items to the website">
    <UButton label="Add Items" />

    <template #body>
      <UForm
        :schema="schema"
        :state="state"
        class="space-y-4"
        @submit="onSubmit"
      >
        <UFormField label="Image" name="file">
          <UFileUpload v-model="state.file" class="min-h-48 pixel"/>
        </UFormField>

        <UFormField label="Name" name="name">
          <UInput v-model="state.name" />
        </UFormField>

        <UFormField label="Type" name="types">
          <UInput v-model="state.types" />
        </UFormField>

        <UFormField label="Quantity" name="quantity">
          <UInput v-model="state.quantity" type="number" />
        </UFormField>

        <UButton label="Submit" type="submit" />
      </UForm>
    </template>
  </UModal>
</template>

<script setup lang="ts">
import type { Items } from "~/components/items/ItemsList.vue";

const config = useRuntimeConfig();

const items = ref<Items[] | null>(null);

onMounted(async () => {
  const data = await $fetch<Items[] | null>(`${config.public.fastApiUrl}/items`, {
    method: "GET",
  });

  if (!data) return;

  items.value = data;
  console.log(items.value)
});
</script>

<template>
  <div>
    <UButton label="Login" to="/login" />
    <ItemsList :items="items" />
  </div>
</template>

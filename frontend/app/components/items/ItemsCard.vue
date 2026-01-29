<script setup lang="ts">
import type { Items } from "./ItemsList.vue";

const props = defineProps<Items>();
</script>

<template>
  <UCard>
    <div class="flex flex-col gap-3">
      <img 
        v-if="props.image_url"
        :src="props.image_url"
        :alt="`Image of ${props.name}`"
        class="object-contain pixel"
      >
      <div>
        <h2>{{ props.name }}</h2>
        <p>{{ props.types }}</p>
        <p>{{ props.quantity }}</p>
      </div>
    </div>
  </UCard>
</template>

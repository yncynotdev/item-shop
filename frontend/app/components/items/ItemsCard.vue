<script setup lang="ts">
import type { Items } from "./ItemsList.vue";

const props = defineProps<Items>();
</script>

<template>
  <UCard>
    <div class="flex flex-col gap-3">
      <img 
        v-if="props.image"
        :src="props.image"
        :alt="`Image of ${props.name}`"
      >
      <div>
        <h2>{{ props.name }}</h2>
        <p>{{ props.types }}</p>
        <p>{{ props.quantity }}</p>
      </div>
    </div>
  </UCard>
</template>

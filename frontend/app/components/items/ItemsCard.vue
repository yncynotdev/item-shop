<script setup lang="ts">
import type { Items } from './ItemsList.vue';

const props = defineProps<Items>();
</script>

<template>
  <UCard>
    <h2>{{props.name}}</h2>
    <p>{{props.types}}</p>
    <p>{{props.quantity}}</p>
  </UCard>
</template>

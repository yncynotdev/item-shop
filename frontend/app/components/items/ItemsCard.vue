<script setup lang="ts">
import type { Items } from './ItemsList.vue';

const props = defineProps<Items>();
</script>

<template>
  <div>
    <h2>{{props.name}}</h2>
    <p>{{props.types}}</p>
    <p>{{props.quantity}}</p>
  </div>
</template>

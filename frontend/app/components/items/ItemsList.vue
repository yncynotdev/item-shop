<script setup lang="ts">
export type Items = {
  id: number | null;
  name: string | null;
  types: string | null;
  quantity: number | null;
  image: string | null;
};

const props = defineProps<{ items: Items[] | null }>();
</script>

<template>
  <ul>
    <li v-for="(item, index) in props.items" :key="index">
      <ItemsCard :name="item.name" :types="item.types" :quantity="item.quantity" />
    </li>
  </ul>
</template>

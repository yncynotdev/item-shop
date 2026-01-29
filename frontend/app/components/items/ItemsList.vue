<script setup lang="ts">
export type Items = {
  id: number | null;
  name: string | null;
  types: string | null;
  quantity: number | null;
  image_url: string | null;
};

const props = defineProps<{ items: Items[] | null }>();
</script>

<template>
  <ul class="flex flex-row gap-5 flex-wrap">
    <li v-for="(item, index) in props.items" :key="index">
      <ItemsCard 
        :name="item.name"
        :types="item.types"
        :quantity="item.quantity"
        :image_url="item.image_url"
      />
    </li>
  </ul>
</template>

<template>
  <UHeader>
    <template #title>
      <p class="font-silkscreen">Items</p> 
    </template>

    <div>
      <ItemsModal />
    </div>

    <template #right>
      <UButton label="Login" to="/login" />
      <UButton label="Sign up" to="/sign-up" />
      <UButton label="Protected" to="/protected" />
    </template>
  </UHeader>
</template>

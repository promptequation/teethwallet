<template>
  <router-view v-slot="{ Component }">
    <transition appear :duration="{ enter: 700, leave: 400 }" mode="out-in" enter-active-class="animated fadeIn"
      leave-active-class="animated fadeOut">
      <component :is="Component" />
    </transition>
  </router-view>
</template>

<script lang="ts">
import { defineComponent } from 'vue';

export default defineComponent({
  name: 'App',
});
</script>

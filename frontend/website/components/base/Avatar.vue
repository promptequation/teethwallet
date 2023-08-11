<template>
  <div
    :class="classes"
    class="base-avatar d-inline-flex"
  >
    <v-avatar
      v-if="outlined"
      :color="color || 'grey lighten-4'"
      :size="outlineSize"
      :style="styles"
      class="base-avatar__outline"
      style="opacity: .4"
    />

    <v-avatar
      :color="color || 'white'"
      :size="size"
      class="base-avatar__avatar"
      v-bind="$attrs"
      v-on="$listeners"
    >
      <img
        :src="icon"
        alt=""
      >
    </v-avatar>
  </div>
</template>

<script>
export default {
  name: "BaseAvatar",

  inject: ["theme"],

  props: {
    color: { type: String, default: '' },
    dark: Boolean,
    icon: { type: String, default: '' },
    outlined: Boolean,
    size: {
      type: [Number, String],
      default: 56
    }
  },

  data: () => ({
    multiply: 6
  }),

  computed: {
    classes () {
      return [this.outlined && "base-avatar--outlined"];
    },
    outlineSize () {
      return Number(this.size) + this.size / this.multiply;
    },
    styles () {
      const margin = this.size / (this.multiply * 2);

      return {
        // Aligns the outline content with the content
        margin: `-${margin}px 0 0 -${margin}px`
      };
    }
  }
};
</script>

<style lang="sass">
.base-avatar
  border-radius: 50%
  position: relative
  overflow: visible

  &__outline
    position: absolute !important
    left: 0
    top: 0

    &.base-avatar--outlined .base-avatar__avatar
      border-width: thin
      border-style: solid

  .theme--light .base-avatar--outlined .base-avatar__avatar
    border-color: rgba(0, 0, 0, .12) !important

  .theme--dark .base-avatar--outlined .base-avatar__avatar
    border-color: rgba(255, 255, 255, .12) !important
</style>

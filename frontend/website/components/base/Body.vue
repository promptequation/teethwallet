<template>
  <component
    :is="tag"
    :class="classes"
    :style="styles"
    class="base-body text-body-1"
    v-bind="$attrs"
    v-on="$listeners"
  >
    <!-- Only use v-html for user data -->
    <div
      v-if="text"
      v-text="text"
    />

    <div
      v-else-if="html"
      v-html="html"
    />

    <slot v-else />
  </component>
</template>

<script>
// Mixins

export default {
  name: 'BaseBody',

  props: {
    html: { type: String, default: '' },
    maxWidth: {
      type: [Number, String],
      default: undefined,
    },
    space: {
      type: [Number, String],
      default: 10,
    },
    tag: {
      type: String,
      default: 'p',
    },
    text: { type: String, default: '' },
  },

  computed: {
    classes () {
      return [
        'grey--text',
        'text--darken-1',
        `text-left`,
        `mb-sm`,
      ]
    },
    styles () {
      return {
        maxWidth: `${this.maxWidth}px`,
      }
    },
  },
}
</script>

<template>
  <div
    :class="classes"
    class="pt-2"
    data-aos="zoom-in"
  >
    <base-avatar
      v-if="icon"
      :color="color"
      :dark="dark"
      :icon="icon"
      :outlined="outlined"
      :size="size"
      class="mb-3 align-self-start"
    />

    <div :class="horizontal && title && 'ml-6'">
      <base-title
        :title="title"
        class="text-uppercase"
        space="3"
      />

      <base-body
        v-if="text || $slots.default"
        :space="horizontal ? 0 : undefined"
        :text="text"
        class="mx-auto"
        max-width="700"
      >
        <slot />
      </base-body>
    </div>
  </div>
</template>

<script>

export default {
  name: 'BaseAvatarCard',

  props: {
    align: {
      type: String,
      default: 'left',
    },
    color: { type: String, default: '' },
    dark: Boolean,
    horizontal: Boolean,
    icon: { type: String, default: '' },
    outlined: {
      type: Boolean,
      default: true,
    },
    space: {
      type: [Number, String],
      default: 8,
    },
    size: {
      type: [Number, String],
      default: 72,
    },
    text: { type: String, default: '' },
    title: { type: String, default: '' },
  },

  computed: {
    classes () {
      const classes = [
        `mb-${this.space}`,
      ]

      if (this.horizontal) {
        classes.push('d-flex')

        if (!this.$slots.default && !this.text) {
          classes.push('align-center')
        }
      }

      return classes
    },
  },
}
</script>

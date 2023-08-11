<template>
  <div>
    <span :style="{ fontSize: `${fontSize}rem` }" class="font-weight-black headline" style="color: #29589C">
      TeethWallet
    </span>
  </div>
</template>

<script>
import { defineComponent } from 'vue'

export default defineComponent({
  name: 'BrandLogo',

  props: {
    fontSize: {
      type: String,
      default: '1.5'
    }
  }
})
</script>

<style scoped>
.font-weight-black {
  font-weight: 900 !important;
}

.headline {
  font-weight: 400;
  line-height: 2rem;
  letter-spacing: normal !important;
  font-family: "Roboto", sans-serif !important;
}

.font-weight-medium {
  font-weight: 500 !important;
}
</style>

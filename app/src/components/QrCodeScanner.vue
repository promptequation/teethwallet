<template>
  <!-- <q-btn color="primary" size="xl" round class="q-mt-lg" icon="mdi-qrcode-scan" @click="startScan" /> -->
  <q-btn color="primary" size="xl" icon="qr_code_scanner" @click="startScan"></q-btn>
</template>

<script lang="ts">
import { defineComponent } from 'vue'
import { useScanner } from 'src/composables'

export default defineComponent({
  props: {
    //true to add new patient / false to add managed patient
    addPatient: {
      type: Boolean,
      default: false,
    },
  },
  setup(props) {
    const { startScan } = useScanner(props.addPatient);

    return {
      startScan,
    };
  },
});
</script>

<template>
  <div id="bottom-bar" class="row text-center items-center">
    <div v-if="!authStore.isDoctor" class="col">
      <div class="div-choice" :class="!current.includes('code') ? 'div-hide' : ''">
        <q-icon color="primary" name="mdi-qrcode" size="lg" @click="selectCode" />
      </div>
      <div v-show="current.includes('code')" class="choice-text">
        <span class="text-primary text-weight-bold">Code</span>
      </div>
    </div>
    <div class="col">
      <div class="div-choice-ball" :class="!current.includes('scan') ? 'div-hide' : ''">
        <q-fab v-if="isDoctorAndPatient" v-model="scan" flat icon="search" color="primary" direction="up" unelevated
          @click="!current.includes('scan') ? (current = 'scan') : ''">
          <q-fab-action color="primary" label="Doctor" padding="10px" style="margin-left: 15px"
            @click="current = 'dscan'" />
          <q-fab-action color="secondary" label="Patient" padding="10px" style="margin-left: 15px"
            @click="current = 'pscan'" />
        </q-fab>
        <q-icon v-else color="primary" name="search" size="lg" @click="selectScan" />
      </div>
      <div v-show="current.includes('scan')" class="choice-text">
        <span class="text-primary text-weight-bold">Scan</span>
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent, watch, ref, computed } from 'vue'
import { useAuthStore } from 'src/stores/auth';
import { usePageStore } from 'src/stores/page';

export default defineComponent({
  setup(props, { emit }) {
    const authStore = useAuthStore()
    const pageStore = usePageStore()

    const profile = computed(() => authStore.user);
    const isDoctorAndPatient = computed(
      () => authStore.isDoctor
    );

    const current = ref(
      authStore.isDoctor ? 'dscan' : 'pcode'
    );
    const scan = ref();

    watch(
      () => current.value,
      () => emit('update:tab', current.value)
    );

    watch(
      () => scan.value,
      () => {
        if (isDoctorAndPatient.value) {
          pageStore.toggleLoading()
        }
      }
    );

    const selectCode = () => {
      current.value = 'pcode';
      if (scan.value) {
        scan.value = !scan.value;
      }
    };
    const selectScan = () => {
      if (authStore.isDoctor) {
        return (current.value = 'dscan');
      }

      current.value = 'pscan';
    };

    return {
      selectScan,
      selectCode,
      current,
      profile,
      scan,
      isDoctorAndPatient,
      authStore,
    };
  },
});
</script>

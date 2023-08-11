<script lang="ts">
import { defineComponent, ref, computed } from 'vue';
import VueQrcode from '@chenfengyuan/vue-qrcode';
import QrCodeScanner from 'src/components/QrCodeScanner.vue';
import CalendarEvents from 'src/components/CalenderEvents.vue';
import NotificationViewer from 'src/components/NotificationViewer.vue';
import { useAuthStore } from 'src/stores/auth';
import { usePageStore } from 'src/stores/page';
import { useAuth } from 'src/composables';

export default defineComponent({
  components: {
    QrCodeScanner,
    VueQrcode,
    CalendarEvents,
    NotificationViewer,
  },

  setup() {
    const authStore = useAuthStore();
    const pageStore = usePageStore();
    const { signOut } = useAuth();

    const profile = computed(() => authStore.user);
    const isDoctor = computed(() => authStore.isDoctor);

    const tab = ref('calendar');
    const updateTab = (tabItem: string) => {
      tab.value = tabItem;
    };

    return {
      tab,
      profile,
      pageStore,
      signOut,
      isDoctor,
      updateTab
    };
  },
});
</script>

<template>
  <q-page class="column justify-center items-center" style="background: linear-gradient(#64b5f6, #29589c)">
    <q-card v-if="profile" square class="shadow-24" id="card">
      <q-card-section class="text-center">
        <q-item class="q-pa-none">
          <q-item-section avatar>
            <q-avatar v-if="profile.avatar">
              <img :src="profile.avatar" />
            </q-avatar>
            <q-avatar v-else color="primary" text-color="white" icon="person"></q-avatar>
          </q-item-section>

          <q-item-section class="text-left">
            <q-item-label>{{ profile.name }}</q-item-label>
          </q-item-section>

          <q-item-section side>
            <notification-viewer />
          </q-item-section>

          <q-item-section side @click="signOut">
            <q-icon size="27px" name="logout" />
          </q-item-section>
        </q-item>
      </q-card-section>
      <q-separator></q-separator>

      <q-tab-panels v-model="tab" animated>
        <template v-if="isDoctor">
          <q-tab-panel name="calendar">
            <calendar-events />
          </q-tab-panel>
          <q-tab-panel name="qr">
            <div class="qr-card flex column justify-center items-center">
              <q-btn color="primary" size="xl" icon="qr_code" @click="updateTab('pcode')"></q-btn>
              <div class="q-px-lg q-py-sm text-body1 text-grey">
                Share the QR code
              </div>
            </div>
          </q-tab-panel>
          <q-tab-panel name="dscan">
            <div class="qr-card flex column justify-center items-center">
              <qr-code-scanner :add-patient="true" />
              <div class="q-px-lg q-py-sm text-body1 text-grey">
                Scan the QR code
              </div>
            </div>
          </q-tab-panel>
          <q-tab-panel name="pcode">
            <div class="qr-card flex column justify-center items-center">
              <vue-qrcode v-if="profile" :value="profile.id" :options="{ width: 250 }" />
              <q-btn class="q-mt-md" label="close" color="warning" @click="updateTab('qr')"></q-btn>
            </div>
          </q-tab-panel>
        </template>
        <template v-else>
          <q-tab-panel name="calendar">
            <calendar-events />
          </q-tab-panel>
          <q-tab-panel name="qr">
            <div class="qr-card flex column justify-center items-center">
              <q-btn color="primary" size="xl" icon="qr_code" @click="updateTab('pcode')"></q-btn>
              <div class="q-px-lg q-py-sm text-body1 text-grey">
                Share the QR code
              </div>
            </div>
          </q-tab-panel>
          <q-tab-panel name="pcode">
            <div class="qr-card flex column justify-center items-center">
              <vue-qrcode v-if="profile" :value="profile.id" :options="{ width: 250 }" />
              <q-btn class="q-mt-md" label="close" color="warning" @click="updateTab('qr')"></q-btn>
            </div>
          </q-tab-panel>
        </template>
      </q-tab-panels>
      <div v-if="isDoctor && tab !== 'pcode'" class="dr-button">
        <q-btn label="Share Access" color="primary" :outline="tab !== 'qr'" @click="updateTab('qr')"></q-btn>
        <q-btn square outline icon="calendar_today" color="primary" :class="tab === 'calendar' ? 'hidden' : ''"
          @click="updateTab('calendar')"></q-btn>
        <q-btn label="Scan Code" color="primary" :outline="tab !== 'dscan'" @click="updateTab('dscan')"></q-btn>
      </div>
      <div v-if="!isDoctor && tab !== 'pcode'" class="patient-button">
        <q-btn square icon="calendar_today" color="primary" :class="tab === 'calendar' ? 'hidden' : ''"
          @click="updateTab('calendar')"></q-btn>
        <q-btn label="Share Access" color="primary" :class="tab === 'qr' ? 'hidden' : ''"
          @click="updateTab('qr')"></q-btn>
      </div>
    </q-card>

    <q-inner-loading :showing="pageStore.loading" />
  </q-page>
</template>

<style lang="scss">
#card {
  width: 90vw;
  margin: 20px 0;
  position: relative;

  .dr-button {
    position: absolute;
    bottom: 2px;
    left: 3px;
    width: 98%;
    display: flex;
    justify-content: space-between;
    padding: 8px;
    margin-bottom: 5px;
  }

  .patient-button {
    position: absolute;
    bottom: 2px;
    width: 100%;
    display: flex;
    justify-content: center;
    padding: 8px;
  }

  .qr-card {
    padding: 8px 0;
    min-height: 440px;
  }
}
</style>
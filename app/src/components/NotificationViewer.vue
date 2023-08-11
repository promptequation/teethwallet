<script lang="ts">
import { defineComponent, computed, onMounted } from 'vue';
import { format, parseISO } from 'date-fns';
import { Device } from '@capacitor/device';
import { PushNotifications } from '@capacitor/push-notifications';
import { useNotificationStore } from 'src/stores/notification';
import { useNotification } from 'src/composables';
import { useAuthStore } from 'src/stores/auth';

export default defineComponent({
  name: 'NotificationViewer',

  setup() {
    const authStore = useAuthStore();
    const notificationStore = useNotificationStore();
    const { fetchNotifications, updateNotification, pushNotification } =
      useNotification();

    const profile = computed(() => authStore.user);
    const notifications = computed(() => notificationStore.getNotifications);

    const notificationIsNotRead = computed(
      () => notifications.value?.filter((item) => !item.isRead).length
    );
    const timeFormat = (date: string) => {
      return format(parseISO(date), 'dd-MM-yy h:mm a');
    };
    const updateSelectedNotification = async (id: number, isRead: boolean) => {
      await updateNotification(id, isRead);
      await fetchNotifications(Number(profile.value?.id));
    };
    onMounted(async () => {
      await fetchNotifications(Number(profile.value?.id));
      await PushNotifications.requestPermissions().then((result) => {
        if (result.receive === 'granted') {
          PushNotifications.register();
        }
      });

      await PushNotifications.addListener('registration', async (token) => {
        const info = await Device.getInfo();
        const id = await Device.getId();
        const name = info.model;
        const user = profile.value?.id?.toString() || '';
        const registrationId = token.value;
        const type = info.platform;
        const deviceId = id.uuid;
        const active = true;
        pushNotification(
          name,
          user,
          registrationId,
          type,
          deviceId,
          active
        );
      });

      await PushNotifications.addListener('registrationError', (error) => {
        console.log(JSON.stringify(error));
      });

      await PushNotifications.addListener(
        'pushNotificationReceived', notification => {
          notificationStore.notifications?.unshift(notification.data);
        }
      );

      PushNotifications.addListener(
        'pushNotificationActionPerformed', notification => {
          console.log(notification.actionId, 'push Notification Action Performed')
        }
      );
    });

    return {
      notifications,
      timeFormat,
      updateSelectedNotification,
      notificationIsNotRead,
    };
  },
});
</script>

<template>
  <div>
    <q-btn round flat dense icon="notifications" size="md">
      <q-badge floating color="red" rounded>
        {{ notificationIsNotRead }}
      </q-badge>
      <q-menu self="top left" max-height="380px" max-width="300px" style="min-height: 200px" transition-show="jump-down"
        transition-hide="jump-up">
        <q-list v-if="notifications?.length === 0" clickable>
          <q-item-section class="text-center" style="height: 200px; width: 300px">
            You have no notifications yet
          </q-item-section>
        </q-list>
        <q-list v-else v-for="(item, index) in notifications" :key="index"
          @click="updateSelectedNotification(item.id, true)" :class="item.isRead === false ? 'bg-grey-13' : ''">
          <q-item clickable>
            <q-item-section v-if="item.notificationType === 'OWNER_REQUEST'">
              Clinic {{ item.company.name }} has sent you an invitation
              <br />
              {{ timeFormat(item.createdAt) }}
            </q-item-section>
            <q-item-section v-if="item.notificationType === 'DOCTOR_REQUEST'">
              Dr. {{ item.createdBy.name }} has sent you an invitation to
              {{ item.company.name }}
              <br />
              {{ timeFormat(item.createdAt) }}
            </q-item-section>
            <q-item-section v-if="item.notificationType === 'DOCTOR_APPROVAL'">
              Dr. {{ item.createdBy.name }} accepted your invitation
              <br />
              {{ timeFormat(item.createdAt) }}
            </q-item-section>
            <q-item-section v-if="item.notificationType === 'OWNER_APPROVAL'">
              Clinic {{ item.company.name }} accepted your invitation
              <br />
              {{ timeFormat(item.createdAt) }}
            </q-item-section>
            <q-item-section v-if="item.notificationType === 'PATIENT_REQUEST_DOCTOR'">
              {{ item.createdBy.name }} wants to give you an access
              <br />
              {{ timeFormat(item.createdAt) }}
            </q-item-section>
            <q-item-section v-if="item.notificationType === 'DOCTOR_ACCEPT_PATIENT_REQUEST'">
              Clinic {{ item.createdBy.name }} accepted your access request
              <br />
              {{ timeFormat(item.createdAt) }}
            </q-item-section>
            <q-item-section v-if="item.notificationType === 'DOCTOR_REVOKE_PATIENT_ACCESS'">
              Your Dentist {{ item.createdBy.name }} has revoked your access to
              his history
              <br />
              {{ timeFormat(item.createdAt) }}
            </q-item-section>
            <q-item-section v-if="item.notificationType === 'PATIENT_REVOKE_DOCTOR_ACCESS'">
              {{ item.createdBy.name }} has revoked your access to his history
              <br />
              {{ timeFormat(item.createdAt) }}
            </q-item-section>
            <q-item-section v-if="item.notificationType === 'APPOINTMENT_CREATED'">
              {{ item.createdBy.name }} has created an appointment for you
              <br />
              {{ timeFormat(item.createdAt) }}
            </q-item-section>
          </q-item>
        </q-list>
      </q-menu>
    </q-btn>
  </div>
</template>

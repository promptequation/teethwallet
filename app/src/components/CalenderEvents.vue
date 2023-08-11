<script>
import { defineComponent, ref, computed, onMounted } from 'vue';
import { format, addMinutes } from 'date-fns'
import { useAppointmentStore } from 'src/stores/appointment';
import { useAuthStore } from 'src/stores/auth';
import { useAppointment } from 'src/composables';

export default defineComponent({
  setup() {
    const authStore = useAuthStore();

    const appointmentStore = useAppointmentStore();
    const { fetchAppointments } = useAppointment();

    const date = ref(`${format(new Date(), "yyyy/MM/dd")}`);

    const profile = computed(() => authStore.user);
    const isDoctor = computed(() => authStore.isDoctor);
    const activeCompany = computed(() => authStore.getActiveCompany);
    const appointments = computed(() => {
      return appointmentStore.getAppointments.map((data) => ({
        doctor: data.doctor,
        patient: data.patient,
        startDate: data.startDate,
        duration: data.duration,
      }));
    });
    const selectedDateAppointment = computed(() => {
      const selectedDate = date.value
      return appointments.value.filter((item) => {
        return format(new Date(item.startDate), "yyyy/MM/dd") == selectedDate
      })
    })

    const eventsFn = (date) => {
      const startDate = appointments.value.map((item) => {
        return format(new Date(item.startDate), "yyyy/MM/dd")
      })
      return startDate.includes(date)
    }

    const timeFormat = (date) => {
      return format(new Date(date), "dd/MM/yy h:mm a");
    };
    const getEndDate = (startDate, duration) => {
      let endDate = addMinutes(new Date(startDate), duration).toISOString();
      return timeFormat(endDate);
    };

    onMounted(async () => {
      if (isDoctor.value) {
        await fetchAppointments({
          patientId: null,
          doctorId: Number(profile?.value?.id),
          companyId: Number(activeCompany.value?.id),
          langId: null,
          isActive: true,
        });
      } else {
        await fetchAppointments({
          patientId: Number(profile?.value?.id),
          doctorId: null,
          companyId: null,
          langId: null,
          isActive: null,
        });
      }
    });
    return {
      date,
      appointments,
      isDoctor,
      selectedDateAppointment,
      timeFormat,
      getEndDate,
      eventsFn
    };
  },
});
</script>

<template>
  <div class="qr-card flex column justify-start items-center" :class="selectedDateAppointment.length > 0 ? 'card-margin' : ''">
    <div>
      <q-date v-model="date" :events="eventsFn" event-color="red" />
      <h6 v-if="selectedDateAppointment.length > 0" class="q-mt-lg q-mb-sm text-primary">Appointment Details</h6>
      <div class="q-mb-md" v-for="appointment in selectedDateAppointment" :key="appointment.id">
        <div class="flex">
          <q-icon class="q-mr-sm q-mt-xs" size="20px" color="primary" name="event" />
          <div class="" >
            <q-badge class="q-pa-none" v-if="!isDoctor" color="white" text-color="black">
              Doctors's Name: {{ appointment.doctor }}
            </q-badge>
            <q-badge class="q-pa-none" v-if="isDoctor" color="white" text-color="black">
              Patient's Name: {{ appointment.patient }}
            </q-badge> <br>
            <q-badge class="q-pa-none" color="white" text-color="black">
              Start Date: {{ timeFormat(appointment.startDate) }}
            </q-badge> <br>
            <q-badge class="q-pa-none" color="white" text-color="black">
              End Date: {{ getEndDate(appointment.startDate, appointment.duration) }}
            </q-badge>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.card-margin{
 margin-bottom: 30px;
}
</style>

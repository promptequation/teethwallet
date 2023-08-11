<template>
  <div id="appointment">
    <v-row>
      <v-col class="tw-flex tw-items-center tw-justify-between">
        <div>
          <v-btn v-can="isDoctor" color="primary" dark to="/admin/appointments/entry">
            {{ $t('appointment.New Appointment') }}
          </v-btn>
        </div>

        <div>
          <v-btn class="ma-2" outlined color="primary" @click="calenderEvent = false">
            <v-icon>mdi-format-list-bulleted-square</v-icon>
            <span class="tw-ml-2 tw-normal-case">{{ $t('appointment.List View') }}</span>
          </v-btn>
          <v-btn class="ma-2" outlined color="primary" @click="calenderEvent = true">
            <v-icon>mdi-calendar-account</v-icon>
            <span class="tw-ml-2 tw-normal-case">{{ $t('appointment.Calendar View') }}</span>
          </v-btn>
        </div>
      </v-col>
    </v-row>
    <v-row>
      <v-col>
        <v-fade-transition>
          <v-card class="mb-7" v-if="calenderEvent">
            <v-toolbar flat>
              <v-toolbar-title> {{ $t('appointment.Calendar-Events') }} </v-toolbar-title>
              <v-spacer></v-spacer>
            </v-toolbar>
            <v-divider></v-divider>
            <div class="pa-4">
              <calendar-events :appointments="appointments" :isDoctor="isDoctor"></calendar-events>
            </div>
          </v-card>
        </v-fade-transition>
        <v-fade-transition>
          <v-card v-if="!calenderEvent" transition="fab-transition">
            <v-card-title class="pa-1">
              <v-text-field v-model="search" solo flat prepend-inner-icon="mdi-magnify"
                :placeholder="$t('appointment.Type something')" hide-details>
              </v-text-field>
            </v-card-title>
            <v-divider> </v-divider>
            <v-card-text class="pa-0">
              <v-data-table :no-data-text="$t('No data found')" v-if="appointments" :headers="header" :items="appointments" :footer-props="{
                'items-per-page-text': $t('Rows per page'),
                'items-per-page-all-text': $t('All')
              }" :loading="loading" :search="search" class="elevation-1 header-text">
                <template #item.patient="{ item }">
                  {{ isDoctor ? item.patient : item.doctor }}
                </template>

                <template #item.survey="{ item }">
                  <nuxt-link v-if="item.survey.edges && item.survey.edges.length > 0"
                    :to="`/admin/appointments/question-survey?appointmentId=${item.id}`">{{
                      item.survey.edges[0].node.survey.name }}</nuxt-link>
                  <span v-else></span>
                </template>

                <template #item.startDate="{ item }">
                  {{ datetime(item.startDate) }}
                </template>
                <template #item.endDate="{ item }">
                  {{ getEndDate(item.startDate, item.duration) }}
                </template>
                <template #item.action="{ item }">
                  <v-btn depressed outlined icon fab dark color="primary" class="mr-0" small title="View"
                    :to="`/admin/appointments/entry?editableId=${item.id}`">
                    <v-icon>mdi-eye</v-icon>
                  </v-btn>
                </template>
              </v-data-table>
            </v-card-text>
          </v-card>
        </v-fade-transition>
      </v-col>
    </v-row>
  </div>
</template>

<script lang="ts">
import {
  ref,
  defineComponent,
  useContext,
  computed,
  useStore,
  useRoute,
  onMounted,
} from "@nuxtjs/composition-api";
import useNuxtTranslator from "~/../composables/useNuxti18n";
import useUser from "~/../composables/useUser";
import calendarEvents from "../../../components/CalendarEvents.vue";
import useAppointment from "../../../../composables/useAppointment";
import useJoinClinic from "~/../composables/useJoinClinic";

export default defineComponent({
  name: "appointment",
  layout: "admin",
  components: { calendarEvents },
  setup() {
    const { $t } = useNuxtTranslator()
    const route = useRoute();
    const { fetchAppointments } = useAppointment();
    const authUser = computed(() => getters["auth/getUserProfile"]);
    const { getters } = useStore();
    const { $dayjs } = useContext();
    const { isDoctor, fetchPatients } = useUser();
    const { fetchActiveCompanyForUser } = useJoinClinic();

    fetchPatients();
    const datetime = (date: string) => {
      return $dayjs(date).format("DD/MM/YY");
    };

    const loading = ref(false);
    const calenderEvent = ref(false);
    const search = ref("");
    const header = computed(() => {
      return [
        isDoctor.value ? { text: `${$t("Patients")}`, value: "patient" } : { text: `${$t("appointment.Doctor")}`, value: "doctor" },
        isDoctor.value && authUser.value.accessSurvey ? { text: `${$t("appointment.Survey")}`, value: "survey" } : '',
        { text: `${$t("Start Date")}`, value: "startDate" },
        { text: `${$t("End Date")}`, value: "endDate" },
        { text: `${$t("Actions")}`, value: "action", sortable: false, align: "center" },
      ];
    });

    const approvedStatus = computed(() => {
      return getters["common/getApprovedStatus"];
    });

    const activeCompany = ref<any>();

    const patients = computed(() => {
      return getters["user/patients"];
    });

    const patientName = (id: any) => {
      const data = patients.value.find((item: any) => {
        return item.id == Number(id);
      });
      return data?.name;
    };

    const appointments = computed(() => getters["appointment/appointments"]);
    const getEndDate = (startDate: string, duration: number) => {
      let endDate = "";
      if (startDate && duration) {
        endDate = $dayjs(startDate).add(duration, "m").toISOString();
      }
      return datetime(endDate);
    };

    const getActiveCompany = async () => {
      const { userCompany } = await fetchActiveCompanyForUser({
        userId: Number(authUser.value?.id),
        groupName: "Doctor",
        statusId: Number(approvedStatus.value?.id),
        isActive: true,
      });

      if (userCompany && userCompany.edges && userCompany.edges.length > 0) {
        activeCompany.value = userCompany.edges[0].node.company;
      }
    };

    onMounted(async () => {
      if (route.value.query?.patient) {
        await fetchAppointments({
          patientId: route.value.query?.patient,
          doctorId: null,
          companyId: null,
          langId: authUser.value?.lang?.id,
          isActive: null
        });
      } else {
        if (isDoctor.value) {
          await getActiveCompany();

          await fetchAppointments({
            patientId: null,
            doctorId: Number(authUser.value?.id),
            companyId: Number(activeCompany.value?.id),
            langId: authUser.value?.lang?.id,
            isActive: true
          });
        } else {
          await fetchAppointments({
            patientId: Number(authUser.value?.id),
            doctorId: null,
            companyId: null,
            langId: authUser.value?.lang?.id,
            isActive: null
          });
        }
      }
    });

    return {
      datetime,
      loading,
      search,
      header,
      appointments,
      isDoctor,
      patientName,
      calenderEvent,
      getEndDate,
    };
  },
});
</script>

<template>
  <v-container fluid class="down-top-padding">
    <!-- <BaseBreadcrumb
      title="StarterPage"
      :icon="page.icon"
      :breadcrumbs="breadcrumbs"
    ></BaseBreadcrumb> -->
    <v-row class="mt-2 pa-4" v-if="isDoctor">
      <v-col cols="12" md="6">
        <v-card class="pa-4" height="100%">
          <v-toolbar dense flat>
            <v-toolbar-title class="primary--text">{{$t('startPage.What is your current clinic?')}}</v-toolbar-title>
          </v-toolbar>
          <v-radio-group @change="setCurrentClinic" v-model="currentClinic" class="ml-6">
            <v-radio color="green" v-for="(clinic,index) in userCompanies" :key="index" :value="clinic.id" :label="clinic.company">
            </v-radio>
          </v-radio-group>
          <v-spacer></v-spacer>
        </v-card>
      </v-col>
      <v-col cols="12" md="6">
        <v-card class="pa-4">
          <div class="px-4 pb-4">
            <calendar-events :key="appointments.length" :appointments="appointments" :isDoctor="isDoctor">
            </calendar-events>
          </div>
        </v-card>
      </v-col>
    </v-row>

    <v-row class="mt-2 pa-4" v-else>
      <v-col cols="12" md="12">
        <v-card class="mb-7 pa-4">
          <div class="px-4 pb-4">
            <calendar-events :key="appointments.length" :appointments="appointments" :isDoctor="isDoctor">
            </calendar-events>
          </div>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>
<script lang="ts">
import {
  reactive,
  ref,
  computed,
  useStore,
  defineComponent,
  onMounted,
  watch,
} from "@nuxtjs/composition-api";
import calendarEvents from "../../components/CalendarEvents.vue";
import useUser from "~/../composables/useUser";
import useAppointment from "../../../composables/useAppointment";
import { compsnyUserType } from '~/types/companyUser'
import useJoinClinic from "~/../composables/useJoinClinic";
import userManageClinic from "~/../composables/useManageClinic";

export default defineComponent({
  layout: "admin",
  components: { calendarEvents },
  setup() {
    const { getters, commit } = useStore();
    const { fetchAppointments } = useAppointment();
    const { fetchAuthUserCompanies, fetchRelatedCompaniesByAuthUser } = useJoinClinic();
    const { setActiveClinic } = userManageClinic()
    const authUser = computed(() => getters["auth/getUserProfile"]);
    const { isDoctor } = useUser();

    const page = reactive({
      icon: null,
    });

    const breadcrumbs = reactive([
      {
        text: "StarterPage",
        disabled: true,
      },
    ]);

    const currentClinic = ref("")

    const approvedStatus = computed(() => {
      return getters['common/getApprovedStatus']
    })

    const appointments = computed(() => getters["appointment/appointments"]);

    const manageFetchAllCompanies = async () => {

      await fetchAuthUserCompanies({
        userId: Number(authUser.value?.id),
        groupName: 'Doctor',
        statusId: Number(approvedStatus.value?.id),
        isOwner: true,
        approvalById: Number(authUser.value?.id),
        langId: authUser.value?.lang?.id
      })

      await fetchRelatedCompaniesByAuthUser({
        userId: Number(authUser.value?.id),
        groupName: 'Doctor',
        statusId: Number(approvedStatus.value?.id),
        isOwner: false,
        approvalById: null,
        langId: authUser.value?.lang?.id
      })
    }

    const userCompanies = computed(() => getters["clinic/getAuthUserCompanies"]);
    const activeClinic = computed(() => getters["clinic/getUserActiveCompany"]);


    watch(activeClinic, async () => {
      currentClinic.value = activeClinic.value?.node.id
      commit('appointment/SET_EMPTY_APPOINTMENTS')
      await fetchAppointments({
        patientId: null,
        companyId: Number(activeClinic.value?.node.company.id),
        doctorId: Number(authUser.value?.id),
        langId: authUser.value?.lang?.id,
        isActive: null
      });
    })

    const setCurrentClinic = () => {
      const companies = userCompanies.value?.filter((clinic: compsnyUserType) => {
        return Number(clinic.id) !== Number(currentClinic.value)
      })
      if (companies && companies.length > 0) {
        companies.forEach((clinic: compsnyUserType) => {
          setActiveClinic({
            companyUserId: Number(clinic.id),
            isActive: false,
            status: 'Approve'
          })
        })
      }
      setActiveClinic({
        companyUserId: Number(currentClinic.value),
        isActive: true,
        status: 'Approve'
      })
      commit('clinic/SET_ACTIVE_CLINIC', currentClinic.value);
    }

    onMounted(async () => {
      if (isDoctor.value) {
        manageFetchAllCompanies()
      } else {
        await fetchAppointments({
          patientId: Number(authUser.value?.id),
          doctorId: null,
          companyId: null,
          langId: authUser.value?.lang?.id,
          isActive: null
        });
      }
    })

    return {
      page,
      breadcrumbs,
      isDoctor,
      appointments,
      userCompanies,
      currentClinic,
      setCurrentClinic,
    };
  },
});
</script>

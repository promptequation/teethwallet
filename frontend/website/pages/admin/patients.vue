<template>
  <v-card id="patients">
    <v-card-text>
      <v-data-table :headers="header" :items="patients" :footer-props="{
        'items-per-page-text': $t('Rows per page'),
        'items-per-page-all-text': $t('All')
         }" sort-by="id" class="contact-listing-app header-text"
          :search="search">
        <template v-slot:top>
          <v-toolbar flat class="mb-8">
            <v-row>
              <v-col cols="12" lg="6">
                <v-text-field v-model="search" append-icon="mdi-magnify" :label="$t('Search Patient')" filled
                  background-color="transparent" hide-details></v-text-field>
              </v-col>
            </v-row>
          </v-toolbar>
        </template>
        <template v-slot:item="{ item }">
          <tr :class="[item.status.name === 'Approve' ? '' : 'grey']">
            <td>{{ item.name }} </td>
            <td>{{ item.dateOfBirth }}</td>
            <td class="text-center">
              <v-btn :disabled="item.status.name === 'Reject'" depressed icon fab color="teal" small title="Open chat"
                @click="openChat(item)">
                <v-icon>mdi-chat</v-icon>
              </v-btn>
            </td>
            <td class="text-center">
              <v-btn :disabled="item.status.name === 'Reject'" depressed icon fab color="primary" small
                title="Open Appointment" @click="openAppointment(item)">
                <v-icon>mdi-eye</v-icon>
              </v-btn>
            </td>
            <td class="text-center">
              <v-btn v-if="item.status.name === 'Approve'" @click="rejectPatientInvitationEvent(item)" depressed icon fab
                dark color="error" class="mr-0" small title="Reject Request">
                <v-icon>mdi-close</v-icon>
              </v-btn>
              <template v-else>
                <v-btn v-if="item.approvalBy && item.approvalBy.id && item.approvalBy.id === authUser.id"
                  @click="acceptPatientInvitationEvent(item)" depressed icon fab dark color="black" class="mr-0" small
                  title="Accept Request">
                  <v-icon>mdi-arrow-u-left-top</v-icon>
                </v-btn>
              </template>
            </td>
          </tr>
        </template>
        <template v-slot:no-data>
          {{ $t('No data found') }}
        </template>
      </v-data-table>
    </v-card-text>

    <ConfirmationDialog ref="confirmation"></ConfirmationDialog>
  </v-card>
</template>

<script lang="ts">
import {
  ref,
  defineComponent,
  useContext,
  computed,
  useStore,
  useRouter,
  onMounted,
} from "@nuxtjs/composition-api";
import useNuxtTranslator from "~/../composables/useNuxti18n";
import useUser from "~/../composables/useUser";
import { Patient } from 'types/user'
import useMyInvitations from "~/../composables/useMyInvitations";
import { patientInvitationsType } from '~/types/companyUser'
import useJoinClinic from "~/../composables/useJoinClinic";
import ConfirmationDialog from "~/components/base/ConfirmationDialog.vue";

export default defineComponent({
  name: "AdminPatient",
  layout: "admin",
  components: { ConfirmationDialog },
  setup() {
    const { $t } = useNuxtTranslator()
    const router = useRouter();
    const { getters } = useStore();
    const { $dayjs } = useContext();
    const { isDoctor } = useUser();
    const authUser = computed(() => getters["auth/getUserProfile"]);
    const { fetchPatientInvitations, acceptPatientInvitation, rejectPatientInvitation } = useMyInvitations();
    const { fetchActiveCompanyForUser } = useJoinClinic();
    const patients = computed(() => {
      return getters["patient/getMyPatients"];
    });
    const approvedStatus = computed(() => {
      return getters["common/getApprovedStatus"];
    });
    const datetime = (date: string) => {
      return $dayjs(date).format("DD/MM/YY");
    };
    const loading = ref(false);
    const search = ref("");
    const confirmation = ref();
    const header = computed(() => {
      return [
        { text: `${$t("Patients")}`, value: "name" },
        { text: `${$t("patients.Birth Date")}`, value: "dateOfBirth" },
        { text: `${$t("patients.Chat")}`, value: "chat", sortable: false, align: "center" },
        { text: `${$t("patients.Check the history")}`, value: "history", sortable: false, align: "center" },
        { text: `${$t("patients.Delete Access")}`, value: "action", sortable: false, align: "center" },
      ]
    });
    const activeCompany = ref<any>();
    const openChat = (user: Patient) => {
      router.push("/admin/messages?patient=" + user.userId);
    };
    const openAppointment = (user: Patient) => {
      router.push("/admin/appointments?patient=" + user.userId);
    };
    const acceptPatientInvitationEvent = async (item: patientInvitationsType) => {
      confirmation.value
        .open(`${$t("dialogue.Permission")}`, `${$t("dialogue.Do you want to accept?")}`, { color: 'red' })
        .then(async (res: boolean) => {
          if (res) {
            await acceptPatientInvitation({
              id: Number(item.id),
              doctorId: null,
              approvalById: Number(authUser.value?.id),
              status: "Approve",
              joinedDatetime: new Date().toISOString(),
              approvalAt: new Date().toISOString(),
              from: "myPatient",
              requestType: 'DOCTOR_ACCEPT_PATIENT_REQUEST'
            });
          }
          return false
        });
    };
    const rejectPatientInvitationEvent = async (item: patientInvitationsType) => {
      confirmation.value
        .open(`${$t("dialogue.Permission")}`, `${$t("dialogue.Do you want to reject?")}`, { color: 'red' })
        .then(async (res: boolean) => {
          if (res) {
            await rejectPatientInvitation({
              id: Number(item.id),
              doctorId: null,
              approvalById: Number(authUser.value?.id),
              status: "Reject",
              approvalAt: new Date().toISOString(),
              from: "myPatient",
              requestType: "DOCTOR_REVOKE_PATIENT_ACCESS"
            });
          }
          return false
        });
    };
    const getActiveCompany = async () => {
      const { userCompany } = await fetchActiveCompanyForUser({
        userId: Number(authUser.value?.id),
        groupName: "Doctor",
        statusId: Number(approvedStatus.value?.id),
        isActive: true
      });
      if (userCompany && userCompany.edges && userCompany.edges.length > 0) {
        activeCompany.value = userCompany.edges[0].node.company;
      }
    };
    onMounted(async () => {
      await getActiveCompany();
      await fetchPatientInvitations({
        companyId: Number(activeCompany.value?.id),
        groupName: "Patient",
        doctorId: Number(authUser.value?.id),
        userId: null,
        statusId: null,
        from: "myPatients"
      });
    });
    return {
      authUser,
      datetime,
      loading,
      search,
      header,
      isDoctor,
      patients,
      openChat,
      acceptPatientInvitationEvent,
      rejectPatientInvitationEvent,
      openAppointment,
      confirmation,
    };
  },
});
</script>

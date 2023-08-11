<template>
  <div>
    <v-row>
      <v-col>
        <v-card>
          <v-card-title class="pa-6">
            <v-row>
              <v-col cols="auto" class="mr-auto">
                <span class="text-h6 blue-grey--text text--darken-3">{{$t('history.General history')}}</span>
              </v-col>
            </v-row>
          </v-card-title>
          <v-card-text>
            <v-data-table :headers="header" :items="appointments" :no-data-text="$t('No data found')" sort-by="id" :footer-props="{
              'items-per-page-text': $t('Rows per page'),
              'items-per-page-all-text': $t('All')
            }" class="contact-listing-app header-text"
              :search="search">
              <template v-slot:top>
                <v-toolbar flat class="mb-8">
                  <v-row>
                    <v-col cols="6" class="mr-auto">
                      <v-text-field v-model="search" append-icon="mdi-magnify" :label="$t('Search')" filled
                        background-color="transparent" hide-details></v-text-field>
                    </v-col>
                  </v-row>
                </v-toolbar>
              </template>
              <template v-slot:item="{ item }">
                <tr class="">
                  <td>{{ datetime(item.startDate) }}</td>
                  <td>{{ item.companyName }}</td>
                  <td>{{ item.doctor }}</td>
                  <td>
                    <v-chip v-for="(priority,index) in item.appointmentprioritySet.edges" :key="index" class="ma-2">
                      {{ priority.node.priority.name }}
                    </v-chip>
                  </td>
                  <td>
                    <span v-for="details in item.appointmentDetails.edges">
                      <v-chip v-if="details && details.node && details.node.tooth" class="ma-2">
                        {{ details.node.tooth.number }}
                      </v-chip>
                    </span>
                  </td>
                  <td>
                    <span v-for="details in item.appointmentDetails.edges">
                      <v-chip v-if="details && details.node && details.node.diagnosis" class="ma-2">
                        {{ details.node.diagnosis.diagnosticlangSet.edges[0].node.name }}
                      </v-chip>
                    </span>
                  </td>
                  <td>
                    <span v-for="details in item.appointmentDetails.edges">
                      <v-chip v-if="details && details.node && details.node.treatment" class="ma-2">
                        {{ details.node.treatment.treatmentlangSet.edges[0].node.name }}
                      </v-chip>
                    </span>
                  </td>
                  <td class="text-center">
                    <v-btn :disabled="!item.isActive" depressed icon fab class="mr-0" small title="Message"
                      @click="openChat(item)">
                      <v-icon>mdi-email</v-icon>
                    </v-btn>
                  </td>
                </tr>
              </template>
            </v-data-table>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>
  </div>
</template>
<script lang="ts">
import {
  defineComponent,
  computed,
  onMounted,
  useStore,
  useContext,
  useRouter,
  ref,
} from "@nuxtjs/composition-api";
import useNuxtTranslator from "~/../composables/useNuxti18n";
import useAppointment from "~/../composables/useAppointment";

export default defineComponent({
  layout: "admin",
  name: "History",
  setup() {
    const { $t } = useNuxtTranslator()
    const router = useRouter()
    const { $dayjs } = useContext();
    const { getters } = useStore();
    const { fetchAppointments } = useAppointment();
    const authUser = computed(() => getters["auth/getUserProfile"]);  
    const header = computed(() => {
      return [
        {
          text: `${$t("Date")}`,
          align: "start",
          sortable: false,
          value: "date",
          width: "150px",
        },
        { text: `${$t("Clinic Name")}`, sortable: false, value: "companyName" },
        { text: `${$t("history.Assigned dentist")}`, sortable: false, value: "doctor" },
        {
          text: `${$t("history.Type of consultation")}`,
          sortable: false,
          value: "consultation",
        },
        { text: `${$t("Tooth")}`, sortable: false, value: "tooth" },
        { text: `${$t("Diagnostic")}`, sortable: false, value: "diagnostic" },
        { text: `${$t("Treatment")}`, sortable: false, value: "treatment" },
        { text: `${$t("history.Message the dentist")}`, sortable: false, value: "massage" },
      ];
    });
    const datetime = (date: string) => {
      return $dayjs(date).format("DD/MM/YY");
    };
    const search = ref("")
    const appointments = computed(() => getters["appointment/appointments"]);
    const openChat = (item: any) => {
      router.push(`/admin/messages?patient=${item.doctorId}&history=${JSON.stringify(item.appointmentDetails.edges)}&startDate=${$dayjs(item.startDate).format("MM/D/YYYY")}`)
    }
    onMounted(async () => {
      await fetchAppointments({
        patientId: Number(authUser.value?.id),
        doctorId: null,
        companyId: null,
        langId: authUser.value?.lang?.id,
        isActive: null
      });
    })
    return {
      search,
      header,
      appointments,
      datetime,
      openChat,
    };
  },
});
</script>

<style lang="scss" scoped>
#main-sidebar {
  box-shadow: 1px 0 20px rgba(0, 0, 0, 0.08);
  -webkit-box-shadow: 1px 0 20px rgba(0, 0, 0, 0.08);

  .v-navigation-drawer__border {
    display: none;
  }

  .v-list {
    padding: 8px 15px;
  }

  .v-list-item {

    &__icon--text,
    &__icon:first-child {
      justify-content: center;
      text-align: center;
      width: 20px;
    }
  }
}
</style>

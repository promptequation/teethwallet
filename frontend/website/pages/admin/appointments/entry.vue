<template>
  <!-- @click="$router.back()" -->
  <validation-observer v-slot="{ handleSubmit, reset }">
    <v-form @submit.prevent="handleSubmit(saveAllAppointment)" @reset.prevent="reset">
      <div id="appointment-entry">
        <v-row>
          <v-col v-if="isDoctor" cols="3">
            <ActionButton class="mb-3 ml-n2" v-if="isDoctor" @click:discard="discardAppointment"
              @click:delete="deleteAppointmentEvent">
            </ActionButton>

            <validation-provider v-slot="{ errors, valid, dirty }" rules="required" vid="patient">
              <v-autocomplete v-model="selectedPatient" :items="patients" outlined chips dense small-chips
                :label="$t('Patients')" item-value="userId" item-text="name" :error-messages="errors"
                :success="valid && dirty" @change="calculatePatientDateOfBirth"></v-autocomplete>
            </validation-provider>

            <date-time outlined v-model="selectedDateTime" :label="$t('Start Date')">
            </date-time>

            <validation-provider v-slot="{ errors, valid, dirty }" rules="required" vid="typeOfAppointment">
              <v-autocomplete v-model="typeOfAppointment" :items="typeOfAppointments" outlined chips
                dense small-chips :label="
                  $t('singleAppointment.Type of appointment')
                " item-value="id" item-text="name" :error-messages="errors"
                :success="valid && dirty"></v-autocomplete>
            </validation-provider>

            <v-autocomplete v-if="authUser.accessSurvey" v-model="selectedSurvey" :items="surveys"
              outlined chips dense small-chips :label="$t('singleAppointment.Survey')" item-value="id" item-text="name"></v-autocomplete>
          </v-col>
          <v-col v-if="isDoctor" cols="3">
            <v-btn class="ma-2 mb-5 tw-opacity-0"></v-btn>

            <validation-provider v-slot="{ errors, valid, dirty }" rules="required" vid="duration">
              <v-combobox v-model="selectedDuration" :items="chooseableTimes"
                :search-input.sync="timeSearch" :label="$t('singleAppointment.Duration')" outlined dense
                @change="appendNewDuration" :error-messages="errors" :success="valid && dirty" item-value="id"
                item-text="text">
                <template v-slot:no-data>
                  <v-list-item>
                    <v-list-item-content>
                      <v-list-item-title>
                        No results matching "<strong>{{
                          timeSearch
                        }}</strong>". Press <kbd>enter</kbd> to
                        create a new one
                      </v-list-item-title>
                    </v-list-item-content>
                  </v-list-item>
                </template>
              </v-combobox>
            </validation-provider>

            <validation-provider v-slot="{ errors, valid, dirty }" rules="required" vid="dentalClinicSpecialitie">
              <v-autocomplete v-model="dentalClinicSpecialitie" :items="specialities" outlined chips
                dense small-chips :label="$t('singleAppointment.Dental clinic specialities')" item-value="id" item-text="name"
                :error-messages="errors" :success="valid && dirty"></v-autocomplete>
            </validation-provider>

            <validation-provider v-slot="{ errors, valid, dirty }" vid="appointmentCode">
              <v-autocomplete hint="Please select problem,decision,treatment and material"
                v-model="appointmentCode" :items="appointmentCodes" outlined multiple dense chips
                :label="$t('singleAppointment.Appointment Code')" item-value="id" item-text="name" :error-messages="errors"
                :success="valid && dirty">
                <template v-slot:selection="data">
                  <v-chip small close v-bind="data.attrs" :input-value="data.selected"
                    :color="getChipColor(data.item.name)" @click:close="
                      removeAppointmentCode(data.item)
                    ">{{ data.item.name }}</v-chip>
                </template>
              </v-autocomplete>
            </validation-provider>
          </v-col>
          <v-col v-else cols="6">
            <v-btn class="mb-5" color="primary" @click="$router.back()">
              {{ $t('singleAppointment.Back') }}
            </v-btn>
            <v-simple-table>
              <template v-slot:default>
                <tbody>
                  <tr>
                    <th>{{ $t('singleAppointment.Doctor Name') }}</th>
                    <td>{{ doctorDetails.name }}</td>
                  </tr>
                  <tr>
                    <th>{{ $t('singleAppointment.Start Date Time') }}</th>
                    <td>
                      {{ selectedDateTimeWithFormat }}
                    </td>
                  </tr>
                  <tr>
                    <th>{{ $t('singleAppointment.Duration') }}</th>
                    <td>{{ getSelectedDuration }}</td>
                  </tr>
                </tbody>
              </template>
            </v-simple-table>
          </v-col>
          <v-col cols="6">
            <div class="ml-2">
              <Under12Savg class="max-width-full" @selectedTeethNumber="selectedTeethNumber" v-if="under12">
              </Under12Savg>
              <Over12Savg class="max-width-full" v-else @selectedTeethNumber="selectedTeethNumber"></Over12Savg>
            </div>
          </v-col>
        </v-row>
        <v-row>
          <v-col>
            <v-card outlined v-if="isDoctor">
              <v-tabs v-model="tabItem">
                <v-tab class="tw-border text-transform-none" v-for="item in tabItems" :key="item.tab">
                  {{ item.tab }}
                </v-tab>
              </v-tabs>

              <v-tabs-items v-model="tabItem">
                <v-tab-item key="one">
                  <v-card outlined>
                    <v-card-text class="pa-0">
                      <v-data-table :headers="header" :items="appointments" :no-data-text="$t('No data found')" :loading="loading" :footer-props="{
                        'items-per-page-text': $t('Rows per page'),
                        'items-per-page-all-text': $t('All')
                        }"
                        class="elevation-1 header-text">
                        <template #item.tooth="{ item }">
                          {{ item.tooth ? item.tooth.number : "" }}
                        </template>
                        <template #item.diagnosis="{ item }">
                          {{ item.diagnosis ? item.diagnosis.diagnosticlangSet.edges[0].node.name : "" }}
                        </template>
                        <template #item.treatment="{ item }">
                          {{ item.treatment ? item.treatment.treatmentlangSet.edges[0].node.name : "" }}
                        </template>
                        <template v-if="addMore" v-slot:body.append>
                          <tr>
                            <td width="200">
                              {{
                                appointment.tooth
                                ? appointment.tooth.number
                                : ""
                              }}
                            </td>
                            <td>
                              <v-combobox class="tw-mt-1" v-model="appointment.diagnosis" :items="diagnostics"
                                :search-input.sync="diagnosisSearch" item-text="name" item-value="id"
                                :label="$t('Diagnostic')" outlined hide-details dense
                                @change="appendNewDiagnostic">
                                <template v-slot:no-data>
                                  <v-list-item>
                                    <v-list-item-content>
                                      <v-list-item-title>
                                        No results matching "<strong>{{
                                          diagnosisSearch
                                        }}</strong>". Press <kbd>enter</kbd>
                                        to create a new one
                                      </v-list-item-title>
                                    </v-list-item-content>
                                  </v-list-item>
                                </template>
                              </v-combobox>
                            </td>
                            <td>
                              <v-combobox class="tw-mt-1" v-model="appointment.treatment" :items="treatments"
                                :search-input.sync="treatmentSearch" item-text="name" item-value="id"
                                :label="$t('Treatment')" outlined hide-details dense
                                @change="appendNewTreatment">
                                <template v-slot:no-data>
                                  <v-list-item>
                                    <v-list-item-content>
                                      <v-list-item-title>
                                        No results matching "<strong>{{
                                          treatmentSearch
                                        }}</strong>". Press <kbd>enter</kbd>
                                        to create a new one
                                      </v-list-item-title>
                                    </v-list-item-content>
                                  </v-list-item>
                                </template>
                              </v-combobox>
                            </td>
                            <td class="text-center">
                              <v-btn v-if="appointments.length" dark color="error" class="mr-0" small title="Cancel"
                                @click="cancel">
                                <v-icon>mdi-minus</v-icon>
                              </v-btn>
                              <v-btn dark color="green" class="mr-0" small title="Save" @click="saveAppointmentDetails">
                                <v-icon>mdi-content-save</v-icon>
                              </v-btn>
                            </td>
                          </tr>
                        </template>
                        <template #item.action="{ item, index }">
                          <v-btn depressed outlined icon fab dark color="teal" class="mr-0" small title="Edit"
                            @click="editAppointmentDetails(item, index)">
                            <v-icon>mdi-pencil</v-icon>
                          </v-btn>
                          <v-btn depressed outlined icon fab dark color="error" class="mr-0" small title="Delete"
                            @click="remove(item, index)">
                            <v-icon>mdi-delete</v-icon>
                          </v-btn>
                          <v-btn v-if="index === appointments.length - 1 && !addMore" depressed outlined icon fab dark
                            color="primary" class="mr-0" small title="Add More" @click="add">
                            <v-icon>mdi-plus</v-icon>
                          </v-btn>
                        </template>
                      </v-data-table>
                    </v-card-text>
                  </v-card>
                </v-tab-item>
                <v-tab-item key="two">
                  <v-card outlined class="tw-p-3">
                    <QuestionExpansion :userId="selectedPatient"></QuestionExpansion>
                  </v-card>
                </v-tab-item>
                <v-tab-item key="three">
                  <v-card class="tw-p-3">
                    <v-textarea v-model="note" class="tw-p-3" counter :label="$t('singleAppointment.Text')" outlined>
                    </v-textarea>
                  </v-card>
                </v-tab-item>
                <v-tab-item key="Files">
                  <v-card outlined>
                    <v-card-text class="pa-0">
                      <v-data-table :headers="appointmentFileHeader" :items="appointmentFiles" :no-data-text="$t('No data found')" :loading="loading" :footer-props="{
                        'items-per-page-text': $t('Rows per page'),
                        'items-per-page-all-text': $t('All')
                      }"
                        class="elevation-1 header-text">
                        <template #item.name="{ item }">
                          {{ item.name }}
                        </template>

                        <template #item.date="{ item }">
                          {{ dateFormat(item.createdAt) }}
                        </template>
                        <template #item.action="{ item, index }">
                          <v-btn v-if="item.id" @click="downloadFile(item)" depressed outlined icon fab dark
                            color="primary" class="mr-0" small title="Download">
                            <v-icon>mdi-download</v-icon>
                          </v-btn>
                        </template>

                        <template v-if="addMore" v-slot:body.append>
                          <tr>
                            <td></td>
                            <td>
                              <v-file-input :label="$t('singleAppointment.File input')" v-model="selectedFiles" outlined
                                dense hide-details multiple placeholder="Upload your files">
                                <template v-slot:selection="{ text }">
                                  <v-chip small label color="primary">
                                    {{ text }}
                                  </v-chip>
                                </template>
                              </v-file-input>
                            </td>
                            <td class="text-center">
                              <v-btn dark color="green" class="mr-0" small title="Save" @click="saveSelectedFiles">
                                <v-icon>mdi-content-save</v-icon>
                              </v-btn>
                            </td>
                          </tr>
                        </template>
                      </v-data-table>
                    </v-card-text>
                  </v-card>
                </v-tab-item>
                <v-tab-item key="FollowUp">
                  <v-card outlined>
                    <v-card-text class="pb-0">
                       <div v-for="(item, index) in appointmentFollowUp">
                         <p> {{index + 1}}.  Follow up date: {{ datetime(item.date) }}</p>
                       </div>
                    </v-card-text>
                  </v-card>
                </v-tab-item>
              </v-tabs-items>
            </v-card>
            <v-card outlined v-else>
              <v-tabs v-model="tabItem">
                <v-tab class="tw-border text-transform-none" v-for="item in tabItems" :key="item.tab">
                  {{ item.tab }}
                </v-tab>
              </v-tabs>
              <v-tabs-items v-model="tabItem">
                <v-tab-item key="one">
                  <v-card outlined>
                    <v-card-text class="pa-0">
                      <v-data-table :headers="header" :items="appointments" :loading="loading" :footer-props="{
                        'items-per-page-text': $t('Rows per page'),
                        'items-per-page-all-text': $t('All')
                      }"
                        class="elevation-1 header-text">
                        <template #item.tooth="{ item }">
                          {{ item.tooth ? item.tooth.number : "" }}
                        </template>
                        <template #item.diagnosis="{ item }">
                          {{ item.diagnosis ? item.diagnosis.diagnosticlangSet.edges[0].node.name : "" }}
                        </template>
                        <template #item.treatment="{ item }">
                          {{ item.treatment ? item.treatment.treatmentlangSet.edges[0].node.name : "" }}
                        </template>
                      </v-data-table>
                    </v-card-text>
                  </v-card>
                </v-tab-item>
                <v-tab-item key="Files">
                  <v-card outlined>
                    <v-card-text class="pa-0">
                      <v-data-table :headers="appointmentFileHeader" :items="appointmentFiles" :no-data-text="$t('No data found')" :loading="loading" :footer-props="{
                        'items-per-page-text': $t('Rows per page'),
                        'items-per-page-all-text': $t('All')
                      }"
                        class="elevation-1 header-text">
                        <template #item.name="{ item }">
                          {{ item.name }}
                        </template>

                        <template #item.date="{ item }">
                          {{ dateFormat(item.createdAt) }}
                        </template>
                        <template #item.action="{ item, index }">
                          <v-btn @click="downloadFile(item)" depressed outlined icon fab dark color="primary" class="mr-0"
                            small title="Download">
                            <v-icon>mdi-download</v-icon>
                          </v-btn>
                        </template>
                      </v-data-table>
                    </v-card-text>
                  </v-card>
                </v-tab-item>
                <v-tab-item key="FollowUp">
                  <v-card outlined>
                    <v-card-text class="pb-0">
                       <div v-for="(item, index) in appointmentFollowUp">
                         <p> {{index + 1}}.  Follow up date: {{ datetime(item.date) }}</p>
                       </div>
                    </v-card-text>
                  </v-card>
                </v-tab-item>
              </v-tabs-items>
            </v-card>
          </v-col>
        </v-row>
      </div>
    </v-form>

    <ConfirmationDialog ref="confirmation" />
  </validation-observer>
</template>

<script lang="ts">
interface TableHeader {
  text?: string;
  value?: string;
  sortable?: boolean;
  align?: string;
  width?: number;
}
interface FileHeaderType {
  text?: string;
  value?: string;
  sortable?: boolean;
  align?: string;
  width?: number;
}

interface oldPriorityType {
  appointmentPriorityId: string | number;
  id: string | number;
  name: string | number;
}

interface oldSpecializationType {
  appointmentSpecializationId: string | number;
  id: string | number;
  name: string | number;
}

interface appointmentCodeType {
  id: string;
  name: string;
  codeType: string;
}

import {
  ref,
  defineComponent,
  reactive,
  onMounted,
  computed,
  useStore,
  useRoute,
  useRouter,
  watch,
  useContext,
} from "@nuxtjs/composition-api";
import useAppointment from "../../../../composables/useAppointment";
import {
  Appointment,
  AppointmentDetail,
  Tooth,
  DoctorDetail,
  PatientType,
} from "~/../../types/appointment";
import useNuxtTranslator from "~/../composables/useNuxti18n";
import useUser from "~/../composables/useUser";
import ActionButton from "~/components/buttons/ActionButton.vue";
import DateTime from "~/components/base/DateTime.vue";
import Under12Savg from "../../../components/base/Under12Savg.vue";
import Over12Savg from "../../../components/base/Over12Savg.vue";
import useMyInvitations from "~/../composables/useMyInvitations";
import useJoinClinic from "~/../composables/useJoinClinic";
import ConfirmationDialog from "~/components/base/ConfirmationDialog.vue";
import userSurvey from "~/../composables/useSurvey";

export default defineComponent({
  name: "AdminAppointmentSingle",
  components: {
    ActionButton,
    DateTime,
    Under12Savg,
    Over12Savg,
    ConfirmationDialog,
  },
  layout: "admin",
  setup() {
    const { app, $dayjs } = useContext();
    const { $t } = useNuxtTranslator()
    const { $toast, $config } = app;
    const editableAppointmentId = ref();
    const { getters } = useStore();
    const route = useRoute();
    const router = useRouter();
    const authUser = computed(() => getters["auth/getUserProfile"]);
    const specialities = computed(() => getters["user/specialities"]);
    const appointmentCodes = computed(() => getters["user/appointmentCodes"]);
    const { fetchSpecialities, fetchAppointmentCodes, isDoctor } = useUser();
    const { fetchPatientInvitations } = useMyInvitations();
    const { fetchSurvey } = userSurvey();

    fetchSpecialities({
      langId: authUser.value?.lang?.id
    });
    fetchAppointmentCodes({
      langId: authUser.value?.lang?.id
    });
    fetchSurvey({
      doctorId: authUser.value?.id,
    });

    const loading = ref(false);
    const search = ref("");

    const header = computed(() => {
      return [
        { text: `${$t("Tooth")}`, value: "tooth" },
        { text: `${$t("Diagnostic")}`, value: "diagnosis" },
        { text: `${$t("Treatment")}`, value: "treatment" },
        isDoctor.value ? {
          text: `${$t("Actions")}`,
          value: "action",
          sortable: false,
          align: "center",
          width: 265,
        } : ''
      ]
    });

    const appointmentFileHeader = computed(() => {
      return [
        { text: `${$t("singleAppointment.Name")}`, value: "name" },
        { text: `${$t("Date")}`, value: "date" },
        {
          text: `${$t("Actions")}`,
          value: "action",
          sortable: false,
          align: "center",
          width: 265,
        },
      ]
    });

    const appointmentFiles = ref<any[]>([]);
    const appointmentFollowUp = ref<any[]>([]);
    const selectedFiles = ref<any[]>([]);
    const finalSelectableAllFiles = ref<any[]>([]);
    const appointments = ref<Appointment[] | AppointmentDetail[]>([]);
    const appointment = reactive<Appointment | AppointmentDetail>({
      id: 0,
      tooth: {},
      diagnosis: "",
      treatment: "",
    });

    const datetime = (date: any) => {
      return $dayjs(date).format("DD/MM/YY h:mm A");
    };

    const discard = ref(false);
    const discardMessage = ref(
      "Something is changed!. Are you want to discard?"
    );
    const toothSearch = ref("");
    const diagnosisSearch = ref("");
    const treatmentSearch = ref("");

    const selectedDateTime = ref("");
    const selectedPatient = ref("");
    const doctorDetails = ref<DoctorDetail>({
      id: "",
      name: "",
    });

    const approvedStatus = computed(() => {
      return getters["common/getApprovedStatus"];
    });

    const activeCompany = ref<any>();

    const typeOfAppointments = computed(
      () => getters["appointment/typeOfAppointments"]
    );
    const patientDiseases = computed(
      () => getters["appointment/patientDiseases"]
    );
    const surveys = computed(() => getters["survey/surveys"]);
    const existingCreatedAppointmentSurvey = ref<any>();
    const selectedSurvey = ref("");

    const dentalClinicSpecialitie = ref("");
    const appointmentCode = ref<string[]>([]);
    const appointmentShortCodes = ref<string[]>([]);
    const getChipColor: any = (item: any) => {
      switch (true) {
        case item.startsWith("P"):
          return "red";
        case item.startsWith("D"):
          return "green";
        case item.startsWith("T"):
          return "primary";
        case item.startsWith("M"):
          return "secondary";
        default:
          return "";
      }
    };
    const removeAppointmentCode = async (item: any) => {
      const index = appointmentCode.value.findIndex((id: string) => item.id === id);
      appointmentCode.value.splice(index, 1);
    };

    const updateAppointmentCodes = (items: any[]) => {
      console.log(items);
    };

    const oldDentalClinicSpecialitie = ref<oldSpecializationType>({
      appointmentSpecializationId: "",
      id: "",
      name: "",
    });
    const typeOfAppointment = ref("");
    const oldTypeOfAppointment = ref<oldPriorityType>({
      appointmentPriorityId: "",
      id: "",
      name: "",
    });
    const confirmation = ref();
    const note = ref("");
    const tabItem:any = ref("");
    const tabItems: any = ref([]);
    const editableIndex = ref(-1);
    const patients = computed(() => {
      return getters["patient/getMyApprovedPatients"];
    });
    const chooseableTimes = computed(() => getters["appointment/durations"]);
    const tooths = computed(() => getters["appointment/tooths"]);
    const treatments = computed(() => getters["appointment/treatments"]);
    const diagnostics = computed(() => getters["appointment/diagnostics"]);
    const selectedDuration = ref();
    const timeSearch = ref("");
    const under12 = ref(true);
    const setTableActionColumnForDoctor = () => {
      if (isDoctor.value) {
        tabItems.value.push({ tab: `${$t("Treatment")}` })
        tabItems.value.push({ tab: `${$t("singleAppointment.Diseases")}`});
        tabItems.value.push({ tab: `${$t("singleAppointment.Notes")}` });
        tabItems.value.push({ tab: `${$t("singleAppointment.Files")}` });
        tabItems.value.push({ tab: `${$t("singleAppointment.Follow Up")}`});
      } else {
        tabItems.value.push({ tab: `${$t("Treatment")}` })
        tabItems.value.push({ tab: `${$t("singleAppointment.Files")}` });
        tabItems.value.push({ tab: `${$t("singleAppointment.Follow Up")}`});
      }
    };
    setTableActionColumnForDoctor();
    const {
      fetchSingleAppointment,
      fetchAppointmentDuration,
      fetchTooths,
      fetchDiagnostics,
      fetchTreatments,
      fetchPatientDiseases,
      fetchPriorities,
      createAppointment,
      updateAppointment,
      deleteAppointment,
      createAppointmentDetails,
      updateAppointmentDetails,
      deleteAppointmentDetails,
      createTooth,
      createDiagnostic,
      createTreatment,
      createAppointmentDuration,
      createAppointmentPriority,
      createAppointmentSpecialization,
      updateAppointmentPriority,
      updateAppointmentSpecialization,
      errors,
      createAppointmentFile,
      createAppointmentSurvey,
      updateAppointmentSurvey,
      deleteAppointmentSurvey,
      createAppointmentShortCode,
      deleteAppointmentShortCode,
    } = useAppointment();

    const { fetchActiveCompanyForUser } = useJoinClinic();

    fetchAppointmentDuration();
    fetchTooths();
    fetchDiagnostics({
      langId: authUser.value?.lang?.id
    });
    fetchTreatments({
      langId: authUser.value?.lang?.id
    });
    // fetchPatientDiseases(patientId)
    fetchPriorities({
      langId: authUser.value?.lang?.id
    });

    watch(selectedDateTime, (newDate: string) => {
      if (!newDate) {
        defineEditableMode();
      }
    });
    const rules = reactive({
      required: (value: any) => !!value || "The field is required.",
      number: (value: any) => {
        const pattern = /^\d+$/;
        return pattern.test(value) || "The field must be number";
      },
    });

    const addMore = ref(false);

    const createNewEditableAppointmentDetails = async (
      appointmentData: AppointmentDetail
    ) => {
      const toothId = appointmentData.tooth ? appointmentData.tooth.id : "";
      const diagnosisId = appointmentData.diagnosis
        ? appointmentData.diagnosis.id
        : "";
      const treatmentId = appointmentData.treatment
        ? appointmentData.treatment.id
        : "";
      const response = await createAppointmentDetails(
        editableAppointmentId.value,
        toothId,
        diagnosisId,
        treatmentId,
        authUser.value?.id,
        authUser.value?.id
      );
      appointments.value.push({
        id: response.createAppointmentDetails.appointmentDetails.id,
        tooth: response.createAppointmentDetails.appointmentDetails.tooth,
        diagnosis:
          response.createAppointmentDetails.appointmentDetails.diagnosis,
        treatment:
          response.createAppointmentDetails.appointmentDetails.treatment,
      });
    };
    const saveAppointmentDetails = async () => {
      let tooth: Tooth = {};
      if (typeof appointment.tooth === "object") {
        tooth = appointment.tooth;
      }
      let diagnosis: any = {};
      if (typeof appointment.diagnosis === "object") {
        diagnosis = {
          "id": appointment.diagnosis.id,
          "diagnosticlangSet": {
            "edges": [
              {
                "node": {
                  "id": null,
                  "name": appointment.diagnosis.name
                }
              }
            ]
          }
        };
      }
      let treatment: any = {};
      if (typeof appointment.treatment === "object") {
        treatment = {
          "id": appointment.treatment.id,
          "treatmentlangSet": {
            "edges": [
              {
                "node": {
                  "id": null,
                  "name": appointment.treatment.name
                }
              }
            ]
          }
        };
      }
      const appointmentData: AppointmentDetail = {
        id: appointment.id,
        tooth,
        diagnosis,
        treatment,
      };
      if (!appointmentData.id && editableAppointmentId.value) {
        createNewEditableAppointmentDetails(appointmentData);
      } else {
        if (editableIndex.value > -1) {
          appointments.value.splice(editableIndex.value, 1, appointmentData);
          editableIndex.value = -1;
        } else {
          appointments.value.push(appointmentData);
        }
      }
      reset();
    };

    const editAppointmentDetails = (item: any, index: number) => {
      editableIndex.value = index;
      appointment.id = item.id ? Number(item.id) : 0;
      appointment.tooth = item.tooth;
      appointment.diagnosis = item.diagnosis;
      appointment.treatment = item.treatment;
    };
    const remove = async (item: any, index: number) => {
      if (item.id) {
        await deleteAppointmentDetails(parseInt(item.id));
        $toast.success(`${ $t('toastMessage.Appointment Successfully Deleted!') }`);
      }
      appointments.value.splice(index, 1);
    };
    const add = () => {
      addMore.value = true;
    };
    const cancel = () => {
      addMore.value = false;
    };
    const reset = () => {
      appointment.id = 0;
      appointment.tooth = {};
      appointment.diagnosis = "";
      appointment.treatment = "";
    };

    const checkAppointmentCodes = () => {
      let getAppointmentProblemCodes = [];
      let getAppointmentDecisionsCodes = [];
      let getAppointmentTreatmentCodes = [];
      let getAppointmentMaterialCodes = [];

      for (const id of appointmentCode.value) {
        const getCode = appointmentCodes.value.find(
          (item: appointmentCodeType) => {
            return parseInt(item.id) === parseInt(id);
          }
        );
        if (getCode && getCode.codeType === "P") {
          getAppointmentProblemCodes.push(getCode);
        } else if (getCode && getCode.codeType === "D") {
          getAppointmentDecisionsCodes.push(getCode);
        } else if (getCode && getCode.codeType === "T") {
          getAppointmentTreatmentCodes.push(getCode);
        } else if (getCode && getCode.codeType === "M") {
          getAppointmentMaterialCodes.push(getCode);
        }
      }

      if (
        getAppointmentProblemCodes.length !==
        getAppointmentDecisionsCodes.length ||
        getAppointmentDecisionsCodes.length !==
        getAppointmentTreatmentCodes.length ||
        getAppointmentTreatmentCodes.length !==
        getAppointmentMaterialCodes.length
      ) {
        return false;
      } else {
        return true;
      }
    };

    const saveAllAppointment = async () => {
      if (!checkAppointmentCodes()) {
        $toast.error(`${ $t('toastMessage.Please select your valid appointment code') }`);
        return;
      }

      const startDate = new Date(selectedDateTime.value).toISOString();
      const duration = selectedDuration.value.number;
      const patientId = parseInt(selectedPatient.value);
      const noteText = note.value;
      const doctorId = authUser.value?.id;
      const createdBy = authUser.value?.id;
      const updatedBy = authUser.value?.id;
      const specialitieId = Number(dentalClinicSpecialitie.value);
      const typeOfAppointmentId = Number(typeOfAppointment.value);
      const companyId = Number(activeCompany.value.id);
      const selectedSurveyId = Number(selectedSurvey.value);

      if (editableAppointmentId.value) {
        await updateAppointmentAndDetails(
          companyId,
          patientId,
          doctorId,
          startDate,
          duration,
          noteText,
          specialitieId,
          typeOfAppointmentId,
          selectedSurveyId,
          createdBy,
          updatedBy
        );

        if (errors.value) {
          $toast.error(
            errors.value.response?.errors[0]?.message || `${ $t('toastMessage.Something is wrong!') }`
          );
        } else {
          $toast.success(`${ $t('toastMessage.Appointment Successfully Updated!') }`);
        }
      } else {
        await storeAppointmentAndDetails(
          companyId,
          patientId,
          doctorId,
          startDate,
          duration,
          noteText,
          specialitieId,
          typeOfAppointmentId,
          selectedSurveyId,
          createdBy,
          updatedBy
        );

        if (errors.value) {
          $toast.error(
            errors.value.response?.errors[0]?.message || `${ $t('toastMessage.Something is wrong!') }`
          );
        } else {
          $toast.success(`${ $t('toastMessage.Appointment Successfully Created!') }`);
        }
      }
      discard.value = false;
      router.push("/admin/appointments");
    };

    const storeAppointmentAndDetails = async (
      companyId: number,
      patientId: number,
      doctorId: number,
      startDate: string,
      duration: number,
      noteText: string,
      specialitieId: number,
      typeOfAppointmentId: number,
      selectedSurveyId: number,
      createdBy: number,
      updatedBy: number
    ) => {
      const res = await createAppointment(
        companyId,
        patientId,
        doctorId,
        startDate,
        duration,
        noteText,
        createdBy,
        updatedBy
      );

      const appointmentId = res.createAppointment.appointment.id;
      appointmentCode.value.forEach(async (code: string) => {
        const codeId = Number(code);
        await createAppointmentShortCode(
          appointmentId,
          codeId,
          createdBy,
          updatedBy
        );
      });

      await createAppointmentPriority({
        appointmentId,
        priorityId: typeOfAppointmentId,
        createdById: createdBy,
        updatedById: updatedBy,
      });

      await createAppointmentSpecialization({
        appointmentId,
        specializationId: specialitieId,
        createdById: createdBy,
        updatedById: updatedBy,
      });

      appointments.value.forEach(
        async (item: Appointment | AppointmentDetail) => {
          let toothId: string | number | undefined = 0;
          if (typeof item?.tooth === "object") {
            toothId = item.tooth?.id;
          }
          let diagnosisId: string | number | undefined = 0;
          if (typeof item?.diagnosis === "object") {
            diagnosisId = item.diagnosis?.id;
          }
          let treatmentId: string | number | undefined = 0;
          if (typeof item?.treatment === "object") {
            treatmentId = item.treatment?.id;
          }
          await createAppointmentDetails(
            appointmentId,
            toothId,
            diagnosisId,
            treatmentId,
            createdBy,
            updatedBy
          );
        }
      );

      if (selectedSurveyId) {
        await createAppointmentSurvey({
          surveyId: selectedSurveyId,
          appointmentId,
          createdById: createdBy,
          updatedById: updatedBy,
        });
      }

      finalSelectableAllFiles.value.forEach(async (file: any) => {
        await createAppointmentFile({
          name: file.name,
          file,
          appointmentId: appointmentId,
          doctorId,
          createdById: createdBy,
          updatedById: updatedBy,
        });
      });
    };

    const updateAppointmentAndDetails = async (
      companyId: number,
      patientId: number,
      doctorId: number,
      startDate: string,
      duration: number,
      noteText: string,
      specialitieId: number,
      typeOfAppointmentId: number,
      selectedSurveyId: number,
      createdBy: number,
      updatedBy: number
    ) => {
      await updateAppointment(
        editableAppointmentId.value,
        companyId,
        patientId,
        doctorId,
        startDate,
        duration,
        noteText,
        updatedBy
      );

      const appointmentId: number = Number(editableAppointmentId.value);

      if (oldTypeOfAppointment.value.appointmentPriorityId) {
        await updateAppointmentPriority({
          id: Number(oldTypeOfAppointment.value.appointmentPriorityId),
          appointmentId,
          priorityId: typeOfAppointmentId,
          createdById: createdBy,
          updatedById: updatedBy,
        });
      } else {
        await createAppointmentPriority({
          appointmentId,
          priorityId: typeOfAppointmentId,
          createdById: createdBy,
          updatedById: updatedBy,
        });
      }

      if (oldDentalClinicSpecialitie.value.appointmentSpecializationId) {
        await updateAppointmentSpecialization({
          id: Number(
            oldDentalClinicSpecialitie.value.appointmentSpecializationId
          ),
          appointmentId,
          specializationId: specialitieId,
          createdById: createdBy,
          updatedById: updatedBy,
        });
      } else {
        await createAppointmentSpecialization({
          appointmentId,
          specializationId: specialitieId,
          createdById: createdBy,
          updatedById: updatedBy,
        });
      }

      const existingAppointmentCodes = appointmentShortCodes.value.map(
        (node: any) => node?.appointmentCode?.id
      );
      const deletableAppointmentCodes = existingAppointmentCodes.filter(
        (x: string) => !appointmentCode.value.includes(x)
      );
      const insertableAppointmentCodes = appointmentCode.value.filter(
        (x: string) => !existingAppointmentCodes.includes(x)
      );

      deletableAppointmentCodes.forEach(async (id: string) => {
        const shortCode: any = appointmentShortCodes.value.find(
          (node: any) => id === node?.appointmentCode?.id
        );
        if (shortCode) {
          await deleteAppointmentShortCode(shortCode.id);
        }
      });
      insertableAppointmentCodes.forEach(async (id: string) => {
        await createAppointmentShortCode(
          appointmentId,
          Number(id),
          createdBy,
          updatedBy
        );
      });
      appointments.value.forEach(
        async (item: Appointment | AppointmentDetail) => {
          const id = item?.id;
          let toothId: string | number | undefined = 0;
          if (typeof item?.tooth === "object") {
            toothId = item.tooth?.id;
          }
          let diagnosisId: string | number | undefined = 0;
          if (typeof item?.diagnosis === "object") {
            diagnosisId = item.diagnosis?.id;
          }
          let treatmentId: string | number | undefined = 0;
          if (typeof item?.treatment === "object") {
            treatmentId = item.treatment?.id;
          }
          await updateAppointmentDetails(
            id,
            appointmentId,
            toothId,
            diagnosisId,
            treatmentId,
            updatedBy
          );
        }
      );

      if (existingCreatedAppointmentSurvey.value?.id && selectedSurveyId) {
        await updateAppointmentSurvey({
          appointmentSurveyId: Number(
            existingCreatedAppointmentSurvey.value.id
          ),
          surveyId: selectedSurveyId,
          appointmentId,
          createdById: createdBy,
          updatedById: updatedBy,
        });
      } else if (
        existingCreatedAppointmentSurvey.value?.id &&
        selectedSurveyId == 0
      ) {
        await deleteAppointmentSurvey({
          appointmentSurveyId: existingCreatedAppointmentSurvey.value?.id,
        });
      } else if (selectedSurveyId) {
        await createAppointmentSurvey({
          surveyId: selectedSurveyId,
          appointmentId,
          createdById: createdBy,
          updatedById: updatedBy,
        });
      }

      finalSelectableAllFiles.value.forEach(async (file: any) => {
        await createAppointmentFile({
          name: file.name,
          file,
          appointmentId,
          doctorId,
          createdById: createdBy,
          updatedById: updatedBy,
        });
      });
    };

    const discardAppointment = () => {
      router.push("/admin/appointments");
    };
    const deleteAppointmentEvent = async () => {
      confirmation.value
        .open(`${$t("dialogue.Delete")}`, `${$t("dialogue.Do you want to delete?")}`, { color: "red" })
        .then(async (res: boolean) => {
          if (res) {
            await deleteAppointment(parseInt(editableAppointmentId.value));
            $toast.success(`${ $t('toastMessage.Your survey already finished') }`);
            router.push("/admin/appointments");
          }
          return false;
        });
    };

    const defineEditableMode = () => {
      if (editableAppointmentId.value) {
        discard.value = true;
      }
    };
    const isEditableMode = () => {
      if (editableAppointmentId.value) {
        return discard.value;
      } else {
        return false;
      }
    };

    const appendNewDuration = async (appendData: string) => {
      defineEditableMode();
      if (typeof appendData === "string") {
        let duration = 0;
        const regex = new RegExp("([0-9]+)|([a-zA-Z]+)", "g");
        const times = appendData.match(regex) || [];
        if (times.length > 2) {
          alert("Please provide valid string");
          selectedDuration.value = "";
        } else {
          const number = times[0];
          const flag = times[1];
          if (flag === "m") {
            duration = Number(number);
          } else if (flag === "h") {
            duration = Number(number) * 60;
          } else {
            alert("Please provide valid string");
            selectedDuration.value = "";
          }
        }
        const res = await createAppointmentDuration(
          duration,
          parseInt(authUser.value?.id)
        );
        selectedDuration.value = res;
      }
    };
    const calculatePatientDateOfBirth = (patientId: number) => {
      let patientData: any;

      if (isDoctor.value) {
        patientData = patients.value.find((item: PatientType) => {
          return Number(item.userId) === Number(patientId);
        });
      } else {
        patientData = authUser.value;
      }

      if (patientData?.dateOfBirth) {
        const dateOfBirth = new Date(patientData.dateOfBirth);
        const currentDate = new Date();

        const date1 = $dayjs(currentDate);
        const date2 = $dayjs(dateOfBirth);
        const year = date1.diff(date2, "y");

        if (year > 12) {
          under12.value = false;
        } else {
          under12.value = true;
        }
      } else {
        $toast.error(`${ $t('toastMessage.User date of birth has not been updated!') }`);
      }
      defineEditableMode();
    };
    const appendNewDiagnostic = async (appendData: string) => {
      defineEditableMode();
      if (typeof appendData === "string") {
        const res = await createDiagnostic(
          appendData,
          parseInt(authUser.value?.id)
        );
        appointment.diagnosis = res;
      }
    };
    const appendNewTreatment = async (appendData: string) => {
      defineEditableMode();
      if (typeof appendData === "string") {
        const res = await createTreatment(
          appendData,
          parseInt(authUser.value?.id)
        );
        appointment.treatment = res;
      }
    };

    const preparEditableData = async () => {
      const res = await fetchSingleAppointment({
        id: parseInt(editableAppointmentId.value),
        langId: authUser.value?.lang?.id
      });

      const appointment = res.appointments?.edges[0].node;
      activeCompany.value = appointment.company;

      const duration = appointment.duration;
      const selectedOldDuration = chooseableTimes.value.find((item: any) => {
        return item.number === duration;
      });
      const specialization = appointment.appointmentspecializationSet.edges;
      const priority = appointment.appointmentprioritySet.edges;
      const appointmentCodeRes = appointment.appointmentshortcodeSet.edges;

      selectedPatient.value = appointment.patient.id;
      selectedDateTime.value = appointment.startDate;
      selectedDuration.value = selectedOldDuration;

      if (specialization && specialization.length > 0) {
        dentalClinicSpecialitie.value =
          specialization[0].node.specialization.id;
        oldDentalClinicSpecialitie.value = {
          appointmentSpecializationId: specialization[0].node.id,
          id: specialization[0].node.specialization.id,
          name: specialization[0].node.specialization.name,
        };
      }

      if (priority && priority.length > 0) {
        typeOfAppointment.value = priority[0].node.priority.id;
        oldTypeOfAppointment.value = {
          appointmentPriorityId: priority[0].node.id,
          id: priority[0].node.priority.id,
          name: priority[0].node.priority.name,
        };
      }

      if (appointmentCodeRes && appointmentCodeRes.length > 0) {
        appointmentCodeRes.forEach((item: any) => {
          appointmentShortCodes.value.push(item?.node);
          appointmentCode.value.push(item?.node?.appointmentCode?.id);
        });
      }

      let appointmentsData: Appointment[] = [];
      appointment.appointmentDetails?.edges.forEach((item: any) => {
        appointmentsData.push({
          id: item.node.id,
          tooth: item.node.tooth ? item.node.tooth : { id: 0, number: "" },
          diagnosis: item.node.diagnosis
            ? item.node.diagnosis
            : { id: 0, name: "" },
          treatment: item.node.treatment
            ? item.node.treatment
            : { id: 0, name: "" },
        });
      });


      let newNote = appointment.note
      if (appointment.appointmentlangSet && appointment.appointmentlangSet.edges?.length > 0) {
        newNote = appointment.appointmentlangSet.edges[0]?.node?.note
      }

      appointments.value = appointmentsData;
      note.value = newNote;
      doctorDetails.value = appointment.doctor;

      let files: any[] = [];
      appointment.appointmentfileSet?.edges.forEach((item: any) => {
        files.push({
          id: item.node.id,
          file: item.node.file,
          name: item.node.name,
          createdAt: item.node.createdAt,
        });
      });
      appointmentFiles.value = files;

      let followUp: any[] = [];
      appointment.appointmentFollowUp?.edges.forEach((item: any) => {
        followUp.push({
          id: item.node.id,
          date: item.node.followUpDate
        });
      });
      appointmentFollowUp.value = followUp;

      if (selectedPatient.value) {
        calculatePatientDateOfBirth(Number(selectedPatient.value));
      }

      if (appointment.appointmentSurvey.edges.length > 0) {
        existingCreatedAppointmentSurvey.value =
          appointment.appointmentSurvey.edges[0].node;
        selectedSurvey.value =
          appointment.appointmentSurvey.edges[0].node.survey.id;
      }
    };
    const getSelectedDuration = computed(() => {
      if (selectedDuration.value) {
        return selectedDuration.value.text;
      }
      return "";
    });

    const dateFormat = (
      dateString: string,
      format: string = "DD/MM/YY"
    ) => {
      return $dayjs(dateString).format(format);
    };

    const selectedDateTimeWithFormat = computed(() => {
      return $dayjs(selectedDateTime.value).format("DD/MM/YY h:mm A");
    });

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
      if(router.currentRoute.query.tab === "follow-up" && isDoctor.value){
        tabItem.value = 4
      } else if(router.currentRoute.query.tab === "follow-up" && !isDoctor.value){
        tabItem.value = 2
      }

      if (appointments.value.length === 0) {
        addMore.value = true;
      }
      // start edit appointments
      editableAppointmentId.value = route.value.query.editableId;

      if (isDoctor.value) {
        await getActiveCompany();

        await fetchPatientInvitations({
          companyId: Number(activeCompany.value?.id),
          groupName: "Patient",
          doctorId: Number(authUser.value?.id),
          userId: null,
          statusId: null,
          from: "myPatients",
        });
      }

      if (editableAppointmentId.value) {
        await preparEditableData();
      }
      // end edit appointments
    });

    const selectedTeethNumber = async (teethNumber: number) => {
      let newTooths = null;

      const findIndex = tooths.value.findIndex((item: Tooth) => {
        return item.number === teethNumber;
      });

      if (findIndex > -1) {
        newTooths = tooths.value[findIndex];
      } else {
        const res = await createTooth(
          teethNumber,
          parseInt(authUser.value?.id)
        );
        newTooths = res;
      }
      appointment.tooth = newTooths;
    };

    const saveSelectedFiles = async () => {
      selectedFiles.value.forEach((item: any) => {
        const nowDate = $dayjs(new Date()).format("DD/MM/YY HH:mm:ss");
        const date = new Date(nowDate.split(" ").join("T"));
        appointmentFiles.value.push({
          id: null,
          file: null,
          name: item.name,
          createdAt: date,
        });
      });
      finalSelectableAllFiles.value = finalSelectableAllFiles.value.concat(
        selectedFiles.value
      );
      selectedFiles.value = [];
    };

    const downloadFile = (item: any) => {
      const fullPath = `${$config.apiClient}/media/${item.file}`;
      const name = item.name.split(".")[0] ?? new Date().getTime().toString();
      fetch(fullPath)
        .then((response) => response.blob())
        .then((imageBlob) => {
          const imageObjectURL = URL.createObjectURL(imageBlob);
          const link = document.createElement("a");
          link.href = imageObjectURL;
          link.setAttribute("download", name);
          document.body.appendChild(link);
          link.click();
          link.remove();
        });
    };

    return {
      loading,
      search,
      header,
      datetime,
      appointmentFollowUp,
      appointments,
      appointment,
      rules,
      addMore,
      saveAppointmentDetails,
      editAppointmentDetails,
      add,
      remove,
      cancel,
      tooths,
      toothSearch,
      diagnostics,
      diagnosisSearch,
      treatments,
      treatmentSearch,
      patients,
      selectedDateTime,
      selectedPatient,
      selectedDuration,
      note,
      timeSearch,
      chooseableTimes,
      saveAllAppointment,
      discardAppointment,
      deleteAppointmentEvent,
      tabItem,
      tabItems,
      appendNewDuration,
      appendNewDiagnostic,
      appendNewTreatment,
      isDoctor,
      calculatePatientDateOfBirth,
      isEditableMode,
      discard,
      discardMessage,
      getSelectedDuration,
      selectedDateTimeWithFormat,
      doctorDetails,
      under12,
      selectedTeethNumber,
      typeOfAppointments,
      dentalClinicSpecialitie,
      appointmentCode,
      getChipColor,
      typeOfAppointment,
      patientDiseases,
      specialities,
      appointmentCodes,
      confirmation,
      appointmentFileHeader,
      appointmentFiles,
      selectedFiles,
      saveSelectedFiles,
      dateFormat,
      downloadFile,
      surveys,
      selectedSurvey,
      editableAppointmentId,
      authUser,
      removeAppointmentCode,
      updateAppointmentCodes,
    };
  },
});
</script>

<style scoped>
.text-transform-none {
  text-transform: none;
}

.max-width-full {
  max-width: 100% !important;
}
</style>

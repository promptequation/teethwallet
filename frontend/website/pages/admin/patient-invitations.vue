<template>
    <v-card id="patients">
        <v-card-text>
            <v-data-table :headers="header" :items="patientInvitations" sort-by="id" :footer-props="{
                'items-per-page-text': $t('Rows per page'),
                'items-per-page-all-text': $t('All')
                              }" class="contact-listing-app header-text"
                :search="search">
                <template v-slot:top>
                    <v-toolbar flat class="mb-8">
                        <v-row class="d-flex justify-space-between align-center">
                            <v-col cols="12" lg="6">
                                <v-text-field v-model="search" append-icon="mdi-magnify"
                                    :label="$t('Search Patient')" filled background-color="transparent"
                                    hide-details></v-text-field>
                            </v-col>
                            <v-col cols="12" lg="6" class="text-right">
                                <v-btn @click="fetchNewPatientRequest" color="primary" class="mr-0" title="Reload">
                                    {{ $t('Reload') }}
                                </v-btn>
                            </v-col>
                        </v-row>
                    </v-toolbar>
                </template>
                <template v-slot:item="{ item }">
                    <tr>
                        <td>{{ item.company }}</td>
                        <td>{{ item.name }}</td>
                        <td>{{ item.email }}</td>
                        <td>{{ item.phone }}</td>
                        <td>{{ datetime(item.requestedAt) }}</td>

                        <td class="text-center">
                            <v-btn @click="acceptPatientInvitationEvent(item)" color="primary" class="mr-0" small
                                title="Accept">
                                {{ $t('actionButtons.Accept') }}
                            </v-btn>
                            <v-btn @click="rejectPatientInvitationEvent(item)" color="error" class="mr-0" small
                                title="Reject">
                                {{ $t('actionButtons.Reject') }}
                            </v-btn>
                        </td>
                    </tr>
                </template>
                <template v-slot:no-data>
                    {{ $t('No data found') }}
                </template>
            </v-data-table>
        </v-card-text>

        <ConfirmationDialog ref="confirmation" />
    </v-card>
</template>

<script lang="ts">
import {
    computed, defineComponent, onMounted, ref, useContext, useStore
} from "@nuxtjs/composition-api";
import useNuxtTranslator from "~/../composables/useNuxti18n";
import useMyInvitations from "~/../composables/useMyInvitations";
import useUser from "~/../composables/useUser";
import useJoinClinic from "~/../composables/useJoinClinic";
import ConfirmationDialog from "~/components/base/ConfirmationDialog.vue";
import { patientInvitationsType } from '~/types/companyUser';

export default defineComponent({
    name: "myInvitations",
    layout: "admin",
    middleware: "doctor",
    components: { ConfirmationDialog },
    setup() {
        const { $t } = useNuxtTranslator()
        const { getters } = useStore();
        const { $dayjs } = useContext();
        const { isDoctor } = useUser();
        const { fetchPatientInvitations, acceptPatientInvitation, rejectPatientInvitation } = useMyInvitations();
        const authUser = computed(() => getters["auth/getUserProfile"]);
        const { fetchActiveCompanyForUser } = useJoinClinic();
        const approvedStatus = computed(() => {
            return getters["common/getApprovedStatus"];
        });
        const pendingStatus = computed(() => {
            return getters["common/getPendingStatus"];
        });
        const activeCompany = ref<any>();
        const managePatientInvitations = async () => {
            fetchPatientInvitations({
                companyId: Number(activeCompany.value?.id),
                groupName: "Patient",
                doctorId: Number(authUser.value?.id),
                userId: null,
                statusId: Number(pendingStatus.value?.id),
                from: "patientInvitations"
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
            await managePatientInvitations();
        });
        const datetime = (date: string) => {
            return $dayjs(date).format("DD/MM/YY");
        };
        const loading = ref(false);
        const search = ref("");
        const confirmation = ref();
        const header = computed(() => {
            return [
                { text: `${$t("Invitations.Company Name")}`, value: "company" },
                { text: `${$t("Invitations.Name")}`, value: "name" },
                { text: `${$t("Email")}`, value: "email" },
                { text: `${$t("Invitations.Phone")}`, value: "phone" },
                { text: `${$t("Invitations.Requested At")}`, value: "requestedAt" },
                { text: `${$t("Actions")}`, value: "action", sortable: false, align: "center" },
            ];
        });
        const patientInvitations = computed(() => {
            return getters["invitation/getAllPatientsInvitations"];
        });
        const fetchNewPatientRequest = async () => {
            managePatientInvitations();
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
                            from: "myInvitation",
                            requestType: "DOCTOR_ACCEPT_PATIENT_REQUEST"
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
                            from: "myInvitation",
                            requestType: ""
                        });
                    }
                    return false
                });
        };
        return {
            datetime,
            loading,
            search,
            header,
            isDoctor,
            patientInvitations,
            fetchNewPatientRequest,
            acceptPatientInvitationEvent,
            rejectPatientInvitationEvent,
            confirmation,
        };
    },
});
</script>

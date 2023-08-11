<template>
    <div>
        <v-row>
            <v-col>
                <v-card>
                    <v-card-title class="pa-6">
                        <v-row>
                            <v-col cols="auto" class="mr-auto">
                                <span class="text-h6 blue-grey--text text--darken-3">{{ $t('accessManagement.Manage the access to my data')
                                }}</span>
                            </v-col>
                        </v-row>
                    </v-card-title>
                    <v-card-text>
                        <v-data-table :headers="header" :items="allRequests" :no-data-text="$t('No data found')" sort-by="id" :footer-props="{
                            'items-per-page-text': $t('Rows per page'),
                            'items-per-page-all-text': $t('All')}"
                            class="contact-listing-app header-text" :search="search">
                            <template v-slot:top>
                                <v-toolbar flat class="mb-8">
                                    <v-row>
                                        <v-col cols="6" class="mr-auto">
                                            <v-text-field v-model="search" append-icon="mdi-magnify"
                                                :label="$t('Search')" filled background-color="transparent"
                                                hide-details></v-text-field>
                                        </v-col>
                                    </v-row>
                                </v-toolbar>
                            </template>
                            <template v-slot:item="{ item }">
                                <tr :class="[item.status.name === 'Approve' ? '' : 'grey']">
                                    <td>{{ item.doctorName }}
                                    </td>
                                    <td>{{ item.joinedDatetime ? datetime(item.joinedDatetime) : '' }}</td>
                                    <td class="text-center">
                                        <v-btn v-if="item.status.name === 'Approve'"
                                            @click="rejectPatientInvitationEvent(item)" depressed icon fab dark
                                            color="error" class="mr-0" small title="Reject Approved">
                                            <v-icon>mdi-close</v-icon>
                                        </v-btn>
                                        <template v-else>
                                            <v-btn
                                                v-if="item.approvalBy && item.approvalBy.id && item.approvalBy.id === authUser.id"
                                                @click="acceptPatientInvitationEvent(item)" depressed icon fab dark
                                                color="black" class="mr-0" small title="Accept Request">
                                                <v-icon>mdi-arrow-u-left-top</v-icon>
                                            </v-btn>
                                        </template>
                                    </td>
                                </tr>
                            </template>
                        </v-data-table>
                    </v-card-text>
                </v-card>
            </v-col>
        </v-row>
        <ConfirmationDialog ref="confirmation" />
    </div>
</template>
<script lang="ts">
import {
    ref,
    defineComponent,
    useContext,
    computed,
    useStore,
    onMounted,
} from "@nuxtjs/composition-api";
import useNuxtTranslator from "~/../composables/useNuxti18n";
import useMyPatient from "~/../composables/useMyPatient";
import useMyInvitations from "~/../composables/useMyInvitations";
import { patientInvitationsType } from '../../../../types/companyUser'
import ConfirmationDialog from "~/components/base/ConfirmationDialog.vue";

export default defineComponent({
    name: "ClinicManagement",
    middleware: "patient",
    setup() {
        const { $t } = useNuxtTranslator()
        const { $dayjs } = useContext();
        const { getters } = useStore();
        const { fetchUserRequest, } = useMyPatient();
        const authUser = computed(() => getters["auth/getUserProfile"]);
        const { acceptPatientInvitation, rejectPatientInvitation } = useMyInvitations();
        fetchUserRequest({
            userId: Number(authUser.value?.id),
            groupName: "Patient"
        });
        const allRequests = computed(() => {
            return getters["patient/getUserRequest"];
        });
        const search = ref("");
        const confirmation = ref();
        const header = computed(() => {
            return [
                { text: `${$t("accessManagement.Doctor Name")}`, value: "doctorName" },
                { text: `${$t("accessManagement.Granted access data")}`, value: "joinedDatetime" },
                { text: `${$t("Actions")}`, sortable: false, align: "center" },
            ]
        });
        const datetime = (date: string) => {
            return $dayjs(date).format("MM/DD/YYYY");
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
                            from: "accessManagement",
                            requestType: ""
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
                            from: "accessManagement",
                            requestType: "PATIENT_REVOKE_DOCTOR_ACCESS"
                        });
                    }
                    return false
                });
        };

        return {
            authUser,
            header,
            allRequests,
            datetime,
            search,
            rejectPatientInvitationEvent,
            acceptPatientInvitationEvent,
            confirmation,
        };
    },
    components: { ConfirmationDialog }
});
</script>

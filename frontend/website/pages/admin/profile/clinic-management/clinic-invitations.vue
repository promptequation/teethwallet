<template>
    <v-card id="patients">
        <v-card-text>
            <v-data-table :headers="header" :items="doctorInvitations" sort-by="id" :footer-props="{
                'items-per-page-text': $t('Rows per page'),
                'items-per-page-all-text': $t('All')}"
                class="contact-listing-app header-text"
                :search="search">
                <template v-slot:top>
                    <v-toolbar flat class="mb-8">
                        <v-row class="d-flex justify-space-between align-center">
                            <v-col cols="12" lg="6">
                                <v-text-field v-model="search" append-icon="mdi-magnify" :label="$t('clinicInvitation.Search Clinic Invitations')"
                                    filled background-color="transparent" hide-details></v-text-field>
                            </v-col>
                            <v-col cols="12" lg="6" class="text-right">
                                <v-btn @click="fetchNewClinicRequest" color="primary" class="mr-0" title="Delete">
                                    {{ $t('Reload') }}
                                </v-btn>
                            </v-col>
                        </v-row>
                    </v-toolbar>
                </template>
                <template v-slot:item="{ item }">
                    <tr>
                        <td>{{ item.company ? item.company : '' }}</td>
                        <td>{{ item.requestedBy ? item.requestedBy : '' }}</td>
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
    ref,
    defineComponent,
    useContext,
    onMounted,
    computed,
    useStore,
} from "@nuxtjs/composition-api";
import useNuxtTranslator from "~/../composables/useNuxti18n";
import useUser from "~/../composables/useUser";
import useMyInvitations from "~/../composables/useMyInvitations";
import { patientInvitationsType } from '../../../../types/companyUser'
import ConfirmationDialog from "~/components/base/ConfirmationDialog.vue";

export default defineComponent({
    name: "ClinicInvitations",
    layout: "admin",
    middleware: "doctor",
    components: { ConfirmationDialog },
    setup() {
        const { $t } = useNuxtTranslator()
        const { $dayjs } = useContext();
        const { getters } = useStore();
        const { isDoctor } = useUser();
        const { fetchClinicInvitations, acceptPatientInvitation, rejectPatientInvitation } = useMyInvitations()

        const authUser = computed(() => getters["auth/getUserProfile"]);
        const getPendingStatus = computed(() => getters['common/getPendingStatus'])
        const doctorInvitations = computed(() => getters["invitation/getClinicInvitations"]);


        const datetime = (date: string) => {
            return $dayjs(date).format("DD/MM/YY");
        };
        const confirmation = ref();
        const loading = ref(false);
        const search = ref("");
        const header = computed(() => {
            return [
                { text: `${$t('Clinic Name')}`, value: "company" },
                { text: `${$t('clinicInvitation.Requested by')}`, value: "requestedBy" },
                { text: `${$t('Actions')}`, value: "action", sortable: false, align: "center" },
            ]
        });

        const fetchNewClinicRequest = async () => {
            await fetchClinicInvitations({
                userId: Number(authUser.value?.id),
                groupName: 'Doctor',
                statusId: Number(getPendingStatus.value?.id),
                isOwner: false
            })
        }

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
                            from: "clinicInvitations",
                            requestType: "DOCTOR_APPROVAL"
                        });
                    }
                    return false;
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
                            status: 'Reject',
                            approvalAt: new Date().toISOString(),
                            from: 'clinicInvitations',
                            requestType: ""
                        })
                    }
                    return false;
                });
        }

        onMounted(async () => {
            await fetchClinicInvitations({
                userId: Number(authUser.value?.id),
                groupName: 'Doctor',
                statusId: Number(getPendingStatus.value?.id),
                isOwner: false
            })
        })

        return {
            datetime,
            loading,
            search,
            header,
            isDoctor,
            doctorInvitations,
            fetchNewClinicRequest,
            acceptPatientInvitationEvent,
            rejectPatientInvitationEvent,
            confirmation,
        };
    },
});
</script>

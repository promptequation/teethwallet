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
                                <v-text-field v-model="search" append-icon="mdi-magnify" :label="$t('doctorInvitation.Search Doctor Invitations')"
                                    filled background-color="transparent" hide-details></v-text-field>
                            </v-col>
                            <v-col cols="12" lg="6" class="text-right">
                                <v-btn @click="fetchNewDoctorRequest" color="primary" class="mr-0" title="Delete">
                                    {{ $t('Reload') }}
                                </v-btn>
                            </v-col>
                        </v-row>
                    </v-toolbar>
                </template>
                <template v-slot:item="{ item }">
                    <tr>
                        <td>{{ item.company ? item.company : '' }}</td>
                        <td>{{ item.name }}</td>
                        <td>{{ item.email }}</td>
                        <td>{{ item.phone }}</td>
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
    watch,
} from "@nuxtjs/composition-api";
import useNuxtTranslator from "~/../composables/useNuxti18n";
import useUser from "~/../composables/useUser";
import useMyInvitations from "~/../composables/useMyInvitations";
import { patientInvitationsType } from '../../../../types/companyUser'
import useJoinClinic from "~/../composables/useJoinClinic";
import ConfirmationDialog from "~/components/base/ConfirmationDialog.vue";

export default defineComponent({
    name: "DoctorInvitations",
    layout: "admin",
    middleware: 'doctor',
    components: { ConfirmationDialog },
    setup() {
        const { $t } = useNuxtTranslator()
        const { getters, commit } = useStore();
        const { $dayjs } = useContext();
        const { isDoctor } = useUser();
        const { fetchAuthUserCompanies } = useJoinClinic();
        const { fetchDoctorInvitations, acceptPatientInvitation, rejectPatientInvitation } = useMyInvitations()

        const authUser = computed(() => getters["auth/getUserProfile"]);
        const approvedStatus = computed(() => getters['common/getApprovedStatus'])
        const getPendingStatus = computed(() => getters['common/getPendingStatus'])
        const getAuthUserCompanies = computed(() => getters['clinic/getAuthUserCompanies'])
        const doctorInvitations = computed(() => getters["invitation/getAllDoctorInvitations"]);

        watch(getAuthUserCompanies, () => {
            getAuthUserCompanies.value.forEach(async (clinic: any) => {
                await fetchDoctorInvitations({
                    companyId: Number(clinic.companyId),
                    groupName: 'Doctor',
                    statusId: Number(getPendingStatus.value?.id),
                })
            })
        })

        const datetime = (date: string) => {
            return $dayjs(date).format("DD/MM/YY");
        };

        const loading = ref(false);
        const search = ref("");
        const confirmation = ref();
        const header = computed(() => {
            return [
                { text: `${$t('Clinic Name')}`, value: "company" },
                { text: `${$t('doctorInvitation.User Name')}`, value: "name" },
                { text: `${$t('doctorInvitation.User Email')}`, value: "email" },
                { text: `${$t('doctorInvitation.User Phone')}`, value: "phone" },
                { text: `${$t('Actions')}`, value: "action", sortable: false, align: "center" },
            ]
        });

        const fetchNewDoctorRequest = () => {
            getAuthUserCompanies.value.forEach(async (clinic: any) => {
                await fetchDoctorInvitations({
                    companyId: Number(clinic.companyId),
                    groupName: 'Doctor',
                    statusId: Number(getPendingStatus.value?.id),
                })
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
                            status: 'Approve',
                            joinedDatetime: new Date().toISOString(),
                            approvalAt: new Date().toISOString(),
                            from: 'doctorInvitations',
                            requestType: "OWNER_APPROVAL"
                        })
                    }
                    return false
                });
        }

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
                            from: 'doctorInvitations',
                            requestType: ""
                        })
                    }
                    return false
                });
        }


        onMounted(async () => {
            commit('invitation/SET_DOCTOR_INVITATIONS_EMPTY')
            await fetchAuthUserCompanies({
                userId: Number(authUser.value?.id),
                groupName: 'Doctor',
                statusId: Number(approvedStatus.value?.id),
                isOwner: true,
                approvalById: Number(authUser.value?.id),
                langId: authUser.value?.lang?.id
            })
        })


        return {
            datetime,
            loading,
            search,
            header,
            isDoctor,
            doctorInvitations,
            fetchNewDoctorRequest,
            acceptPatientInvitationEvent,
            rejectPatientInvitationEvent,
            confirmation,
        };
    },
});
</script>
